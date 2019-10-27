simple Queue
{
    gates:
        input in;
        output out[2];
}

simple Sink
{
    gates:
        input in;
        output out;
}

simple Gen
{
    gates:
        input in[2];
        output out;
}
network Tictoc1
{
    @display("bgb=250,131");
    submodules:
        A: Gen {
            @display("p=37,65");
        }
        B: Queue {
            @display("p=105,65");
        }
        C: Sink {
            @display("p=201,34");
        }
        D: Sink {
            @display("p=201,92");
        }
    connections:
        A.out --> {  delay = 50ms; } --> B.in;
        B.out[0] --> {  delay = 100ms; } --> C.in;
        B.out[1] --> {  delay = 100ms; } --> D.in;
        C.out --> {  delay = 50ms; } --> A.in[0];
        D.out --> {  delay = 50ms; } --> A.in[1];
}
