#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Gen : public cSimpleModule
{
    protected:
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;
};

class Queue : public cSimpleModule
{
    protected:
        virtual void handleMessage(cMessage *msg) override;
};

class Sink : public cSimpleModule
{
    protected:
        virtual void handleMessage(cMessage *msg) override;
};


Define_Module(Gen);
Define_Module(Queue);
Define_Module(Sink);

void Gen::initialize(){
    simtime_t time = 150;
    for(int i = 0; i < 1000000; i++){
        cMessage *msg = new cMessage("Data");
        sendDelayed(msg,time,"out");
    }
}

void Gen::handleMessage(cMessage *msg){
    send(msg, "out");
}

void Queue::handleMessage(cMessage *msg){
    static int k = 0;
    send(msg, "out", k);
    if(k == 0)
            k = 1;
    else
        k = 0;
}

void Sink::handleMessage(cMessage *msg){
    send(msg, "out");
}
