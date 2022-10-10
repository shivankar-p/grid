netgenerate --grid --grid.x-number=5 --grid.y-number=5 --grid.x-length=500 --grid.y-length=1000 -o grid.net.xml
netconvert -s grid.net.xml --plain-output-prefix plain
/usr/share/sumo/tools/xml/xml2csv.py plain.edg.xml
python3 $SUMO_HOME/tools/randomTrips.py -n grid.net.xml --fringe-factor 5 -r dua.rou.xml -p 1 --end 3600 --binomial 3 --validate --weights-prefix all_edges_example --random
