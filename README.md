# ORSIS-ClickSoftware2017
The ORSIS-ClickSoftware2017 optimization challenge, see: 
http://orsis.net.technion.ac.il/orsis-challenge/2017-2/

The 2017 OC challenge is a cooperation between ORSIS and ClickSoftware, designed to strengthen ties between industry and academia in the field of Operations Research. It is an opportunity to expose students and researchers to practical problems, and for ClickSoftware to be involved with the research community. This is the second year that ORSIS is presenting a challenge with a leading company. 
The first part of this document states the challenge problem and the second provides instructions for participants.



Problem definition
~~~~~~~~~~~~~~~~~~

1. The OC challenge problem is to propose an efficient schedule of mobile resources (e.g., engineers) to perform maintenance tasks over a large geographical area, as can be seen below. 

2. The file Tasks.csv defines 1546 tasks, providing task ID, required (resource) skill ID, geographical location, earliest and latest start time (all during the same day), and nominal task duration. The last two columns (added 13/2/17) are the earliest and latest start times, counted in minutes from midnight (e.g., 08:00 = 480). In this sense they are equivalent to the earliest and latest start time, but are easier to "work with". Each task requires one skill. 

3. The file Resources.csv defines 242 resources, providing resource ID, geographical location of the resource, and resource efficiency. The nominal duration of the task will be divided by the efficiency to determine actual assignment’s duration (e.g., efficiency 2.0 means all tasks assigned to this resource will take half of their nominal time). The resources should start and finish work at their location. The start working time of all resources is 8:00 am and the end working time is 5:00 pm (i.e., shifts’ duration is 9 hours for all resources). 

4. A resource is able to start travel only from the beginning of his shift and must finish travel by the end of his shift (i.e., travel not before 8:00 am and not after 5:00 pm).

5. The file Skills.csv defines the skills that each resource has, providing resource ID and skill ID. Each resource can have more than one skill.

6. Distances should be calculated based on aerial calculations:
      Input: Origin_Lat, Origin_Long, Destination_Lat, Destination_Long.
      Output: Distance (km)
      Distance = 
                  ACOS(SIN(Origin_Lat * 3.14159265358979 / 180.0)
                  * SIN(Destination_Lat * 3.14159265358979 / 180.0)
                  + COS(Origin_Lat * 3.14159265358979 / 180.0)
                  * COS(Destination_Lat * 3.14159265358979 / 180.0)
                  * COS((Destination_Long - Origin_Long) * 3.14159265358979 / 180.0)) * 6371

Assume that all resources drive at an average speed of 50 km/h. 

7. There are four objectives, lexicographically ordered by their importance: 
(7a) The main objective is to maximize the number of tasks scheduled within their feasible earliest and latest start time. 
(7b) The secondary objective is to minimize the total travel time.
(7c) The third objective is to maximize the number of tasks scheduled in their safe time. Safe time is defined from the earliest start time up to 30 minutes before the latest start time (in order to minimize the risk of showing up late due to traffic jams and other considerations).
(7d) Finally, the fourth objective is to minimize the difference between the longest and shortest shifts among all resources, for the sake of fairness. 
Lexicographic order means that each objective becomes relevant only in case of ties in all more important objectives.  

8. In the following example we present a small problem instance with a solution (the solution is not necessarily optimal).  
(8a) The input is presented here: http://orsis.net.technion.ac.il/files/2017/01/OC_2017_Challenge_Example.zip.
(8b) A solution is presented here: http://orsis.net.technion.ac.il/files/2017/01/OC_2017_Challenge_Example_Solution.zip
These files are also present in the github repository under "sample_files": 
https://github.com/adisarid/ORSIS-ClickSoftware2017/sample_files/

The solution consists of three columns: resource ID, task ID, and start time.



Participation rules
~~~~~~~~~~~~~~~~~~~

1.	Participation 
The Operations Research community is invited to take part in this challenge. Participation is allowed for teams of (one or) several members. 
Not allowed to participate:  
(1a) ORSIS president, ORSIS representatives in the prize committee and students under their supervision. 
(1b) ClickSoftware employees. 

2. Registration 
(2a) The OC challenge registration will be possible in this form (http://sgiz.mobi/s3/b952399c7a73), also available in the website http://orsis.net.technion.ac.il/orsis-challenge/2017-2/. 
(2b)	Each team must register to the challenge to get access to the input data. Upon registration, each team should provide a team name, the names and affiliation of the members and one e-mail address for correspondence. 

3. Solution submission: 
(3a) Solutions must be submitted as a csv file in the format described above by Sunday, May 7th, noon (Israel time), to oc.challenge2017@gmail.com with the subject “Solution - <Team name>”.  
(3b) The solution file name should be the <team_name>.csv. Each solution will be accompanied by 2-4-page summary of the algorithm/method. 
(3c) A Python script that validates the solution will be made available in the competition web-site. The teams are asked to use it to check their solutions before submitting. 
(3d) Upon submission, at least one member of the team must be an ORSIS member. 

4. Additional conditions 
(4a) The names, solutions and reports of the leading teams will be published in the competition and in ORSIS web-sites.  
(4b) The winning teams will be required to present their accomplishment in a dedicated session in the 2017 annual ORSIS meeting on May 21st -22nd , at Bar-Ilan University (http://orsis.net.technion.ac.il/2016/08/24/coming-conf/). 
(4c)	The prizes will be awarded on this occasion. 
(4d)	The copyright for all submitted materials and algorithms will remain the authors’. 

5. Prizes: 
(5a) The prizes are the generous contribution of ClickSoftware. 
(5b) The winner(s) will be determined by the challenge prize committee, comprised of ClickSoftware and ORSIS representatives.  
(5c) The Winner of the OC challenge will be awarded 4000 NIS and a certificate. 	  
(5d) An additional prize of 1500 NIS and a certificate will be awarded to the best team whose members are all students. Such teams are required to submit a statement that the team’s work was not led by a faculty member. 
(5e) The committee may decide to give a certificate of an honorable mention to one additional team. 

6. Winning criteria: 
(6a) The main winning criterion will be the objective function value of the solution (as described in the problem definition section). However, the committee will also consider the solution methods, its robustness to stochasticity of task durations and travel times, and its methodological contribution. 
(6b) The competing teams are allowed to use commercial and open source general purpose solvers (such as CPLEX or SCIP) but solutions produced by software packages that are dedicated to movable workers planning (such as ClickSoftware) will not be accepted. 
(6c) The competing teams may use reasonable computing resources (brute force solutions are not likely to win anyway). 

