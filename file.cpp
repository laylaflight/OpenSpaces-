#include <iostream>
using namespace std;


int value = 0x82fa9281;
int main(){
for (int i = 0; i < 32; i++)
{
    bool set = (value & 0x1) != 0;
    value >>= 1;

    Console.WriteLine("Bit set: {0}", set);
}
}