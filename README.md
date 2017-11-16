## Log-Analysis

### Overview

This a python tool designed to analyze certain server log based on PostgreSQL and produce simple, meaningful resport.

### How to run

####Dependencies:  

[Python v3 ](https://www.python.org/download/releases/3.0/)  
[psycopg 2](http://initd.org/psycopg/download/)

#### Installation 

1. Install [VirtualBox v5.1](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
2. Install [Vagrant](https://www.vagrantup.com/downloads.html):  
3. Download Vagrant configuration by using following commands:
		`$ git clone https://github.com/udacity/fullstack-nanodegree-vm` 
		`$ cd vagrant`
3. Download server log data frorm [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and place it in the aforementioned vagrant directory.
4. Download this repository.  
		`$ git clone https://github.com/shuchenliu/log-analysis.git`
	
### SQL Views

Before running the python program, you need to define 2 views in PostgreSQL.

Connect to the `news` database:  
`$ psql -d news`

Define first view *ViewStats* for **article and author analysis**:  

```sql
create view ViewStats as
    select articles.title, articles.author, count(*)
    from articles join log
    on substr(log.path, 10) = articles.slug
        and method='GET'
        and status='200 OK'
    group by articles.title, articles.author
    order by count(*) desc;
```

Define second view *ErrorRate* for **error analysis**:  

```sql
create view ErrorRate as 
    select cast(time as date) as date, 
           round(
               sum(case when status!='200 OK' then 1 else 0 end) * 100 ::decimal / count(*)
               ,2) as errorRate 
    from log 
    group by date order by errorRate;
```


### Output
Upon running the command  
	`$ python log_analysis.py`  
you would expect the terminal to display the report answering 3 data analysis questions, like indicated in the `log-analysis.txt` file.
