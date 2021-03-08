# -*- coding: utf-8 -*-
"""
Created on Sun Mar 7 12:48:10 2021

@author: kasrakhadem
"""
import sys
#Non messing with conditional import! :D

from selenium import webdriver
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import numpy as np
from datetime import date
import json
from tweepy import API,OAuthHandler


if sys.argv[1]=="3":
    
    # Initializing the webdriver
    options = webdriver.ChromeOptions()
        
        #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
        #options.add_argument('headless')
        
        #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path="C:\\Users\\kasra\\Notebooks\\NSFRAPID\\Selenium\\chromedriver.exe", options=options)
    driver.set_window_size(1120, 1000)
    #for the error
    # time.sleep(10)    
    
    #list of locations
    
    
    def get_jobs(driver,target_url, num_jobs,duplicate_limit,output):
          
        driver.get(target_url)
        count=0
        file=open(output,"a")
        #read the previous jobs
        try:
            
            try:
                #changed to read the actual data
                #shouldn't be uft-8
                log=pd.read_csv(output,usecols =['add_id','emp_id','order_id'], encoding='utf-8')
            except:
                log=pd.DataFrame(columns=['add_id','emp_id','order_id'])
                print("logfile didn't open!")
          
            
            
            #track number of duplicates
            dup=0
            duplimit=duplicate_limit
            #removed job description
            cols=["Job Title", "id","emp_id","order","Company Name","Location","scrape_date"]
            temp_job=[]
            
            # print("Progress:", end = ' ')
            while count < num_jobs and dup<=duplimit:  #If true, should be still looking for new jobs.
                
                #Let the page load. Change this number based on your internet speed.
                #Or, wait until the webpage is loaded, instead of hardcoding it.
                time.sleep(7)
        
                
                #Going through each job in this page
                job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
                
                for job_button in job_buttons:  
                    # print("|", end = '')
                    if count >= num_jobs or dup>=duplimit:
                        file.close()
                        #qlog_pd=pd.DataFrame(qlog)    
                        #qlog_pd.to_csv(logfile) 
                        return (count,dup)
                    
                    add_id=job_button.get_attribute("data-id")
                    #employer id for making a better key for searching
                    emp_id=job_button.get_attribute("data-emp-id")
                    #Don't know what is this yet but might be the relative priority 
                    order_id=job_button.get_attribute("data-ad-order-id")
                    #adding the dup check here
                    if np.int64(add_id) in list(log['add_id']) and np.int64(emp_id) in list(log['emp_id']) and np.int64(order_id) in list(log['order_id']):
                        dup +=1
                        
                    
                    else:
                        # this has to be before the click:
                        #doesn't work with headless, possibly a js running
                        
                        
                        #job_button.click()  
                        
                        #changed to js because of the new changes:
                        driver.execute_script("arguments[0].click();",job_button)
                        time.sleep(.5)
                        collected_successfully = False
                        
                        while not collected_successfully:
                            try:
                                company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                                location = driver.find_element_by_xpath('.//div[@class="location"]').text
                                job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                                #job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
            
                                collected_successfully = True
                            except:
                                time.sleep(5)
            
                        
                        sctime=datetime.now()
                    
                        #check if it is in the privious logfile moved to top
                    
                        
                        #writing everythin directly to file
                        #append to reduce rw
                        
                        temp_job.append([job_title,add_id,emp_id,order_id,company_name,location,sctime])
                        
                        
                        #queue for the log
                        #has to be int otherwise doesn't work
                        log=log.append({'add_id': np.int64(add_id) ,'emp_id': np.int64(emp_id),'order_id': np.int64(emp_id)}, ignore_index=True)
                        
                    
                    count +=1 
                #Clicking if it is the last page
                if driver.find_element_by_xpath('.//li[@class="next"]//a').get_attribute('innerHTML').find("disabled") != -1:
                    break
                
                #Clicking on the "next page" button
                try:
                    #Changed to js
                    #driver.find_element_by_xpath('.//li[@class="next"]//a').click()
                    driver.execute_script("arguments[0].click();",driver.find_element_by_xpath('.//li[@class="next"]//a'))
                except NoSuchElementException:
                    print("Something fishy: Needed {}, got {}".format(num_jobs, count))
                    break
                #writing at the end of the page
                if len(temp_job) !=0:
                    jobs_df=pd.DataFrame(temp_job,columns=cols)
                    jobs_df.to_csv(file, header=False, index=False,line_terminator='\n', encoding='utf-8')
                    temp_job=[]
                
              
        except:
        # qlog_pd=pd.DataFrame(qlog)    
        # qlog_pd.to_csv(logfile)
            if len(temp_job) !=0:
                    jobs_df=pd.DataFrame(temp_job,columns=cols)
                    jobs_df.to_csv(file, header=False, index=False,line_terminator='\n', encoding='utf-8')
    
            file.close()
            
        return (count,dup)
    
    
    
    #Parameters:
    job=int(sys.argv[4])      #900         #no need to change this
    limit=int(sys.argv[3])    #899    #I start with 30 (a page)
    # log=40      #keep the last 40 jobs
    link=sys.argv[2]
    datafile=sys.argv[1]
    
    pstart=datetime.now()
    print("starting...")
    start=datetime.now()
    print("Starting time: ", start)
    print("\n found %3d jobs and %3d duplicates" %get_jobs(driver,link, job,limit,datafile))

    pend=datetime.now()
    print("total runtime: ", pend-pstart)
elif sys.argv[1]=="4":
    print(sys.argv[1])
    ACCESS_TOKEN = "K123456789"
    ACCESS_TOKEN_SECRET = "K123456789"
    CONSUMER_KEY = "K123456789"
    CONSUMER_SECRET = "K123456789"
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    tweet=API(auth)
    trend=tweet.trends_place(2464592)
    filename = "results"+date.today().strftime("%d%m%Y")+".json"
    file=open(sys.argv[2],'a')
    json.dump(trend,file)
else:
    
    print("use python 3 for part 3 and python 4 for question 4")