#include <iostream>

#include <FLAC++/encoder.h>

int main(int argc, char **argv)
{
    FLAC::Encoder::File encoder;

    if(!encoder) {
        std::cerr << "ERROR: allocating encoder\n" << std::endl;
        return 1;
    }

    encoder.finish();
    return 0;
}
