
#include <getopt.h>
#include <iostream>
#include <string.h>

#include <unistd.h> // Clock management
#include <sys/timerfd.h> // Clock management
#include <zmq_addon.hpp> // socket communication with Python

// hapticomm headers
#include "HaptiCommConfiguration.h"
#include "waveform.h"
#include "ad5383.h"
#include "utils.h"
#include "alphabet.h"

bool read_python_command(zmq::socket_t * sub, std::string & motion_type, std::vector<std::vector<std::string>> * actuatorslist2D);
void parse_command(std::string msg, std::string & motion_type, std::vector<std::vector<std::string>> * actuatorslist2D);
std::vector<std::vector<std::string>> parse_actuators_array(std::string msg);
std::vector<std::string> parse_actuators_line(std::string msg);

int setOpt(int *argc, char *argv[], const char *& cfgSource, const char *& scope);
static void usage();

/*
 * https://brettviren.github.io/cppzmq-tour/index.html
 */
int main(int argc, char *argv[]) {
  std::cout << "AD5383 (hapticomm driver): Beginning..." << std::endl;

  // define the hapticomm library (waveforms and actuators managements)
  const char * cfgSource = "hapticommlib/4_configuration/configBlack.cfg";
  HaptiCommConfiguration * cfg = new HaptiCommConfiguration();
  DEVICE * dev  = new DEVICE();
  WAVEFORM * wf   = new WAVEFORM();
  ALPHABET * alph = new ALPHABET();
	cfg->configure(cfgSource, dev, wf, alph);

  // define communication with the Python script for stimuli manager
  zmq::context_t ctx(1);
  zmq::socket_t subscriber(ctx, zmq::socket_type::sub);
  subscriber.connect("tcp://localhost:5556");
  subscriber.set(zmq::sockopt::subscribe, ""); //opens ALL envelopes

  /* define the current program as high priority (for realtime communication with AD5383)
	struct timespec t;
	struct sched_param param;
	param.sched_priority = sched_get_priority_max(SCHED_FIFO);
	if(sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
			perror("sched_setscheduler failed");
			exit(-1);
	}
  */

  // initialise AD5383 driver
  AD5383 ad;
  waveformLetter trajectories;
  int durationRefresh_ns = (1/(double) alph->getFreqRefresh_mHz()) * ms2ns; // period in nanoseconds
  if (!ad.spi_open()) exit;
  ad.configure();
  ad.execute_trajectory(alph->getneutral(), durationRefresh_ns);

  
  std::string motion_type;
  std::vector<std::vector<std::string>> actuatorslist2D;
  std::cout << "AD5383 (hapticomm driver): Listening..." << std::endl;
  while(read_python_command(&subscriber, motion_type, &actuatorslist2D)) {
    /*
    std::cout << std::endl << "motion_type: " << motion_type << std::endl;
    for (int len=0; len<actuatorslist2D.size(); len++){
      for (int w=0; w<actuatorslist2D[0].size(); w++){
        std::cout << actuatorslist2D[len][w] << ", " << std::flush;
      } 
      std::cout << std::endl;
    }
    */
    std::cout << "trajectories..." << std::flush;
    trajectories = alph->createSymbol(motion_type, actuatorslist2D);
    std::cout << "created." << std::endl;
    ad.execute_selective_trajectory(trajectories, durationRefresh_ns);
    std::cout << "execute_selective_trajectory done." << std::endl;
  }

  for (int security=0; security<10; security++){
    ad.execute_trajectory(alph->getneutral(), durationRefresh_ns);
  }

  delete cfg;
  delete dev;
  delete wf;
  delete alph;
  return 0;
}


bool read_python_command(zmq::socket_t * sub, std::string & motion_type, std::vector<std::vector<std::string>> * actuatorslist2D) {
  static const std::string stop_trigger("SIG_END_PROGRAM");
  static zmq::message_t msg;
  std::string msg_str;

  sub->recv(msg); // default: zmq_recv() function shall block until the request can be satisfied. 
  msg_str = msg.to_string();
  msg_str.erase(std::remove(msg_str.begin(), msg_str.end(), '\n'), msg_str.cend());
  
  std::cout << "C++: command received: " << msg_str << std::endl;

  if (stop_trigger.compare(msg_str) == 0) {
    return false;
  }
  
  parse_command(msg_str, motion_type, actuatorslist2D);
  return true;
}

void parse_command(std::string msg, std::string & motion_type, std::vector<std::vector<std::string>> * actuatorslist2D) {
  static const std::string delimiter(";");
  size_t start = 0; 
  size_t stopped = 0; 

  int width, length = 0;
  int word_count = 0;

  while ((stopped = msg.find(delimiter, start)) != std::string::npos) {
    //std::cout << "(parsing)word_count: " << word_count << std::endl;
  
    switch (word_count) {
			case 0: // type of motion
        motion_type = msg.substr(start, stopped-start);
        //std::cout << "(parsing)motion_type: " << motion_type << std::endl;
				break;
			case 1: // width of the stimulus
        width = std::stoll(msg.substr(start, stopped-start));
        //std::cout << "(parsing)width: " << width << std::endl;
				break;
			case 2: // length of the stimulus
        length = std::stoll(msg.substr(start, stopped-start));
        //std::cout << "(parsing)length: " << length << std::endl;
				break;
		}
    // set up the next word
    start = stopped + 1; 
    word_count++;
    // if the actuator list has been reached, extract it and exit the function
    if (word_count == 3) {
      break;
    }
  }
  *actuatorslist2D = parse_actuators_array(msg.substr(start));
}

std::vector<std::vector<std::string>> parse_actuators_array(std::string msg) {
  static const std::string delimiter(";");
  size_t start = 0; 
  size_t stopped = 0;

  //std::cout << "actuators list: " << msg << "." << std::endl;
  std::vector<std::vector<std::string>> actuators2D;
  while ((stopped = msg.find(delimiter, start)) != std::string::npos) {
    actuators2D.push_back(parse_actuators_line(msg.substr(start, stopped-start)));
    // set up the next word
    start = stopped + 1; 
  }
  actuators2D.push_back(parse_actuators_line(msg.substr(start)));

  return actuators2D;
}

std::vector<std::string> parse_actuators_line(std::string msg) {
  static const std::string delimiter(",");
  size_t start = 0; 
  size_t stopped = 0;

  //std::cout << "actuators line: " << msg << "." << std::endl;
  std::vector<std::string> acts;
  while ((stopped = msg.find(delimiter, start)) != std::string::npos) {
    acts.push_back(msg.substr(start, stopped-start));
    // set up the next word
    start = stopped + 1; 
  }
  acts.push_back(msg.substr(start));

  return acts;
}



/* 
 * getopt_long() refers to '-' hyphen for a single alphanumeric symbol option, '--' for a long option 
 * getopt_long_only() check '-' for long option first, if not found check a single alphanumeric symbol option
 */
int setOpt(int *argc, char *argv[], const char *& cfgSource, const char *& scope) {
	string help = "help";
	string cfg_long = "cfg";
	string scope_long = "scope";
	
	static struct option long_options[] =
	{
		{help.c_str(), 			no_argument, NULL, 'h'},
		{cfg_long.c_str(), required_argument, NULL, 'c'},
		{scope_long.c_str(), optional_argument, NULL, 'p'},
		{NULL, 0, NULL, 0}
	};

	// character of the option
	int c;
	// Detect the end of the options. 
	while ((c = getopt_long(*argc, argv, "chp", long_options, NULL)) != -1) {
		switch (c) {
			case 'c':
        std::cout << "config found!" << std::endl;
        std::cout << optarg << std::endl;
        std::cout << cfgSource << std::endl;
				cfgSource = optarg;
				break;
			case 'p':
				scope = optarg;
				break;
			case 'h':
				usage();
				return -1;
			case '?':
				/* getopt_long already printed an error message. */
				break;
			default:
				abort();
		}
	}
	
	return 0;
}

static void usage() {
	fprintf(stderr,
            "\n"
	    "usage: listener_AD5383 <options>\n"
            "\n"
	    "The <options> can be:\n"
	    "  -h, --help\n"
		"\tPrint this usage statement\n"
	    "  -c, --cfg <source>\n"
		"\tParse the specified configuration file\n"
	    "  --scope <name>\n"
		"\tApplication scope in the configuration source\n\n");
	exit(1);
}



