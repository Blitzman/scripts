#!/bin/bash

programname=$0

function usage {
    echo "usage: $programname [input video] [start time] [time] [output GIF] [width] [FPS]"
    exit 1
}

if [ $# != 6 ]; then
  usage
fi

ffmpeg -y -ss $2 -t $3 -i $1 -vf fps=$6,scale=$5:-1:flags=lanczos,palettegen palette.png
ffmpeg -ss $2 -t $3 -i $1 -i palette.png -filter_complex "fps=$6,scale=$5:-1:flags=lanczos[x];[x][1:v]paletteuse" $4
rm palette.png
