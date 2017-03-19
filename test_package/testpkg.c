#include <stdio.h>

#include <FLAC/stream_encoder.h>

int main(int argc, char **argv)
{
    FLAC__StreamEncoder* encoder = 0;

    if((encoder = FLAC__stream_encoder_new()) == NULL) {
        fprintf(stderr, "ERROR: allocating encoder\n");
        return 1;
    }

    FLAC__stream_encoder_finish(encoder);
    return 0;
}
