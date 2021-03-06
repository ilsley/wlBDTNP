(* Mathematica script *)

outputDir=FileNameJoin[{ParentDirectory[DirectoryName[$InputFileName]],"final"}];
inputDir=FileNameJoin[{ParentDirectory[DirectoryName[$InputFileName]],"intermediate"}];
bdtnpdata=Import[FileNameJoin[{inputDir,"BDTNPVirtualEmbryo.tsv"}]];

importedEmbryo=Dataset[Association[Thread[bdtnpdata[[1]]->#]]&/@bdtnpdata[[2;;]]];
nucleiNeighbours=Import[FileNameJoin[{inputDir,"BDTNPNucleusNeighbours.tsv"}]][[2;;]];
nucleiGraph=Thread[#[[1]]<->#[[3;;]]]& /@ nucleiNeighbours //Flatten //Graph //SimpleGraph;
eveStripesCohort3=importedEmbryo[Select[#cohort==3\[And]#eve>0.2&]];
nucleiNotInEveStripes=importedEmbryo[Select[#cohort==3\[And]#eve <=0.2&],"nucleus_id"] //Normal;
eveCC=ConnectedComponents[Subgraph[nucleiGraph,eveStripesCohort3[All,"nucleus_id"] //Normal]];
eveCCMedianX=Map[Function[subgraphids,Median@eveStripesCohort3[Select[MemberQ[subgraphids,#"nucleus_id"]&],"x"]],eveCC];
eveCCOrdered=Prepend[eveCC[[Ordering[eveCCMedianX]]],nucleiNotInEveStripes];
nucleiStripesAssoc=MapIndexed[Map[Function[nucid,Association[{"stripe"->First[#2]-1,"nucleus_id"->nucid}]],#1]&,eveCCOrdered] //Flatten;

embryoAssoc=JoinAcross[Normal@importedEmbryo,nucleiStripesAssoc,"nucleus_id"] ;
filestream=OpenWrite[FileNameJoin[{outputDir,"BDTNP.wl"}]]
WriteString[filestream,"(* Generated by "<>FileNameTake[$InputFileName]<>" *)\n\n"]
WriteString[filestream,"BeginPackage[\"BDTNP`\"]\n\n"]

(* At the first time of writing, Datasets added directly via PutAppend produced Context issues when reading back in later. *)
PutAppend[Definition[embryoAssoc],filestream];
PutAppend[Definition[nucleiGraph],filestream];
PutAppend[Definition[nucleiStripesAssoc],filestream];
WriteString[filestream,"EndPackage[]\n\n"]
Close[filestream]

