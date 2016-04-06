A pdf table extracter and presents the extracted data in csv format.
getting output in the form of json, xml is currently in testing stage.

Dependencies
1)pdftohtml ---this tool must be installed and must be used for making the given pdf to xml
        <strong>command:-- pdftohtml filename.pdf -xml </strong>
        output--filename.xml <br>
2)lxml  parser is required <br>
3)beautiful soup 4 is required


 steps:--

1)After converting given pdf to xml using pdftohtml tool using above command then 

2)use command : -- (change directory to where submit.py is placed)<br>
     <strong> python code.py -f filename.xml > /path/to/destination_filename.csv</strong>

   i.e the output csv is redirected to destination filename using ">" operator and /path/to/ :-is the path where final csv output must be copied to

[ the above I have tested and used in linux --ubuntu 14.04 ]

