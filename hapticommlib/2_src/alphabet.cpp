/*
 * alphabet.cpp
 *
 *  Created on: 7 apr. 2016
 *      Author: basilou
 */ 

#include "alphabet.h"
#include<ncurses.h>

using namespace std;




ALPHABET::ALPHABET(){}

ALPHABET::ALPHABET(DEVICE * _dev, WAVEFORM * _wf) :
        dev(_dev), 
        wf( _wf){}

ALPHABET::~ALPHABET() {}



void 
ALPHABET::configure() 
{
    configure_neutral();
    dictionnary.clear();
}

void 
ALPHABET::configure(DEVICE * _dev, WAVEFORM * _wf) 
{
    dev = _dev;
    wf = _wf;
    
    configure();
}






std::string 
ALPHABET::getlistSymbols() 
{
    return listSymbols;
}

std::vector<std::vector<uint16_t>> 
ALPHABET::getneutral() 
{
    return neutral_statement;
}


waveformLetter
ALPHABET::getl(std::string l) 
{
    // searching for the letter l
    it_dictionnary = dictionnary.find(l);
    if (it_dictionnary != dictionnary.end())
    {
        return it_dictionnary->second.data;
    }
    else
    {// if not found, return an empty vector 
        return dictionnary.find("~")->second.data;
    }
}

waveformLetter
ALPHABET::getl(char l) 
{
    std::string lstring(1, l);
    return getl(lstring);
}


double 
ALPHABET::getFreqRefresh_mHz() 
{
    return wf->getFreqRefresh_mHz();
}

/* creation: 2022/07/09
 * @function: createSymbol
 * used for the hapticomm efficacy psychophysics experiment
 * The requirement was to use an 2D array of actuators ID rather than a vector.
 * @return the intended waveformLetter
 */
waveformLetter ALPHABET::createSymbol(std::string motion, std::vector<std::vector<std::string>> actuatorsList2D) {
    waveformLetter wfLetter;  // std::multimap<uint8_t, std::vector<uint16_t>>
    struct motion m = wf->getMotion(motion);
    struct actuator * act_current = new actuator();
    std::vector<uint16_t> trajectory;
    
    int dir, amplmax, amplmin, neutral = 0;
    
    /*
    std::cout << std::endl << std::endl << "(createSymbol)motion: " << motion << std::endl;
    for (int len=0; len<actuatorsList2D.size(); len++){
      for (int w=0; w<actuatorsList2D[0].size(); w++){
        std::cout << actuatorsList2D[len][w] << ", " << std::flush;
      }
      std::cout << std::endl;
    }
*/
    for(int ll=0; ll<actuatorsList2D.size(); ++ll) {
        for(int w=0; w<actuatorsList2D[0].size(); ++w) {
            // extract current actuator's information
            *act_current = dev->getActuator(actuatorsList2D[ll][w]);
            dir = act_current->windingDirection;
            neutral = act_current->vneutral;
            amplmax = act_current->vmax - neutral;
            amplmin = neutral - act_current->vmin;

            // define the trajectory for the current line and actuator
            trajectory.resize(m.data[ll].size());
            // adapt the trajectory to actuator's characteristics
            std::transform(m.data[ll].begin(), m.data[ll].end(), trajectory.begin(), 
                [neutral, amplmax, amplmin, dir](double i){ int ampl = (i<0)?amplmin:amplmax; return (uint16_t)((i*dir*ampl)+neutral); });
            // save the current trajectory in the waveform
            wfLetter.insert(waveformLetterPair(act_current->chan, trajectory)); 
            // clear the trajectory vector for the next actuator
            trajectory.clear();
        }
    }
    
    return wfLetter;
}


/* Private :
 * 
 * create the adequat motion for the letter/symbol
 */
bool 
ALPHABET::insertSymbol(struct symbol s)
{
    std::pair<std::map<std::string, symbol>::iterator,bool> ret;
    struct motion       m = wf->getMotion(s.motion);
    struct actuator *   act = new actuator();
    waveformLetter          wfLetter;
    std::vector<uint16_t>   mv;
    int dir;
    int amplmax;
    int amplmin;
    int neutral;
    
    for(int cpt=0; cpt<s.actList.size(); ++cpt)
    {
        *act = dev->getActuator(s.actList[cpt]); //current actuator
        dir = act->windingDirection;
        neutral = act->vneutral; //neutral value
        amplmax = act->vmax - neutral; //amplitude max value
        amplmin = neutral - act->vmin;  //amplitude min value
        mv.resize(m.data[cpt].size());
        std::transform(m.data[cpt].begin(), m.data[cpt].end(), mv.begin(), //transform the signal from
            [neutral, amplmax, amplmin, dir](double i){ //+1/-1 to +/-amplitude
                int ampl = (i<0)?amplmin:amplmax;
                return (uint16_t)((i*dir)*ampl+neutral);});
        
        wfLetter.insert(waveformLetterPair(act->chan, mv)); //add vector to the map
        mv.clear(); //clear the temporary vector
        
        /*
         * 
        std::cout   << "motion name='" << s.id
                    << "'|| actuator name='" << s.actList[cpt]
                    << "'; neutral=" << neutral
                    << "; amplmax=" << amplmax
                    << "; amplmin=" << amplmin 
                    << std::endl;
                    
         */
    }
    
    s.data = wfLetter;
    ret = dictionnary.insert(std::pair<std::string, struct symbol>(s.id, s)); //add symbol to the map
    
    
    listSymbols.append(s.id);
    return ret.second;
}




void 
ALPHABET::configure_neutral() {
    std::vector<uint16_t> temp; 
    temp.push_back(AD5383_DEFAULT_NEUTRAL);
    temp.push_back(AD5383_DEFAULT_NEUTRAL);
    
    for(int i=0; i<AD5383::num_channels; i++)
    {
        neutral_statement.push_back(temp);
    }
}



void 
ALPHABET::informationsSymbol(std::string id)
{
    symbol s = dictionnary[id];
    std::cout << "Motion:" 
            << "\n    id: " << s.id  
            << "\n    motion: " << s.motion
            << "\n    actOverlap: " << std::fixed << s.actOverlap
            << "\n    actuators' name: " ;
    for(auto it=s.actList.begin(); it != s.actList.end(); ++it)
    {
        std::cout << *it << ", ";
    }
    std::cout << std::endl;
       
}

void 
ALPHABET::printData(std::string id)
{
    waveformLetter wfl = getl(id);
    std::vector<uint16_t> data;
    int numSample, c, i;
    
    
    std::cout.precision(5);
    informationsSymbol(id);
    for(auto it=wfl.begin(); it!=wfl.end(); ++it)
    {
        c = it->first;
        data.insert(data.begin(), it->second.begin(), it->second.end());
        
        numSample = data.size();
        std::cout << "channel n�" << c << "/32, numSample= " << numSample << std::endl; 
        for(i=0; i<numSample; i++)
        {
            std::cout << std::fixed << data[i] << "; "; 
        }
        std::cout << std::endl;
        data.clear();
    }   
}


