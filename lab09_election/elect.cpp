#include <string.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

struct rr // symbolic process
{
    int index;
    int id;
    int f;
    char state[10];
} proc[10];

int main()
{
    int i,j,k,m,n, temp;
    char str[10];
    cout << "Enter the total number of processes: ";
    cin >> n;
    for(i = 0; i < n; i++)
    {
        proc[i].index;
        cout << "\nEnter id of process " << i << ": ";
        cin >> proc[i].id;
        strcpy(proc[i].state, "active");
        proc[i].f = 0;
    }

    // sorting
    for(i = 0; i < n-1; i++)
    {
        for(j = 0; j < n-1; j++)
            if(proc[j].id > proc[j+1].id)
            {
                temp = proc[j].id;
                proc[j].id = proc[j+1].id;
                proc[j+1].id = temp;
            }
    }

    cout << "Sorted processes:\n";
    for( i = 0; i < n; i++)
        printf("[%d] %d\n", i, proc[i].id);

    int init, temp1, temp2;
    int arr[10];
    strcpy(proc[n-1].state, "inactive");

    for(i = 0;i < n; i++)
        proc[i].f=0;

    cout<<"\nEnter the process number who intialised election: ";
    cin >> init;

    temp2 = init;
    temp1 = init+1;
    i = 0;
    while(temp2 != temp1)
    {
        if(strcmp(proc[temp1].state, "active") == 0 && proc[temp1].f == 0)
        {
            cout << "Process id " << proc[init].id << " send message to " << proc[temp1].id << "\n";
            proc[temp1].f = 1;
            init = temp1;
            arr[i] = proc[temp1].id;
            i++;
        }
        if(temp1 == n)
            temp1 = 0;
        else
            temp1++;
    }

    cout << "Process id " << proc[init].id << " send message to " << proc[temp1].id << "\n";

    arr[i] = proc[temp1].id;
    i++;
    int max = -1;

    for(j = 0; j < i; j++)
        if(max < arr[j])
            max = arr[j];

    cout<<"\nProcess id " << proc[max].id << " selected as leader.\n";
}