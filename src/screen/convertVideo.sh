cd /home/leno/gitProjects/Curriculum_HFO/src/screen
ffmpeg -f image2 -r 4 -i step%d.png -vcodec mpeg4 -y movie.mp4
rm step*
