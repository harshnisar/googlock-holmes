#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import libsolvemedia
import webapp2
import cgi
import datetime
import urllib
import jinja2
import os
import time

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


from google.appengine.ext import db
from google.appengine.api import users

questions=dict([
      (1,"1."),
      (2,"2."),
      (3,"3."),
      (4,"4."),
      (5,"5."),
      (6,"6."),
      (7,"7."),
      (8,"8."),
      (9,"9."),
      (10,"10.A question before every journey in .."),
      (11,"11."),
      (12,"12.What are these?"),
      (13,"13.He is adopted"),
      (14,"14."),
      (15,"15."),
      (16,"16."),
      (17,"17."),
      (18,"18. Plan for today?"),
      (19,"19."),
      (20,"20"),
      (21,"20"),




      ])

answers=dict([
      (1,"nickiminaj"),
      (2,"wikipedia"),
      (3,"memes"),
      (4,"shinchan"),
      (5,"samsung"),
      (6,"twoandahalfmen"),
      (7,"avengers"),
      (8,"herbiefullyloaded"),
      (9,"pope"),
      (10,"pokemon"),
      (11,"dhamaal"),
      (12,"broomsticks"),
      (13,"kungfupanda"),
      (14,"batman"),
      (15,"xkcd"),
      (16,"friends"),
      (17,"jenniferlawrence"),
      (18,"300"),
      (19,"snapchat"),
      (20,"zerodarkthirty"),
      (21,""),



      ])

image=dict([
      (1,"30"),
      (2,"138"),
      (3,"786"),
      (4,"420"),
      (5,"840"),
      (6,"666"),
      (7,"543"),
      (8,"729"),
      (9,"438"),
      (10,"339"),
      (11,"169"),
      (12,"270"),
      (13,"432"),
      (14,"524"),
      (15,"916"),
      (16,"111"),
      (17,"813"),
      (18,"615"),
      (19,"528"),
      (20,"177"),
      (21,""),
 


      ])

#Model defination of a team

class Team(db.Model):
  """Models a team entry with an name 1 , name 2 and user id."""
  member1 = db.StringProperty()
  member2 = db.StringProperty()
  score   = db.IntegerProperty()
  email   = db.StringProperty()
  uid     = db.StringProperty()
  level   = db.IntegerProperty()
  tname   = db.StringProperty()
  passes  = db.IntegerProperty()
  tstamp  = db.DateTimeProperty(auto_now=True)
  daiict  = db.BooleanProperty(default=False)




class MainHandler(webapp2.RequestHandler):
    def get(self):
##        template = jinja_environment.get_template('templates/index.html')
##        self.response.out.write(template.render())
          self.redirect('/site/index.html')

#this displays the form      
class Register(webapp2.RequestHandler):
    def get(self):
        
        user = users.get_current_user()
        team=Team.all()
        #if already registered, redirect to start
        if user:
            team.filter('uid =',user.user_id())
            for teams in team:
              if teams is not None:
                #team already registered
                
                self.response.write('''<html> <p align='center' style="font-family:Garamond"><font color='red' size=32 > <b> You have already registered </b> </font></p> </html>''')
            

            #self.response.out.write('Hello, ' + user.nickname())
            #form comes here
            
            form=open('register.html', 'r').read()
            self.response.write(form)
            
                    
        else:
            self.redirect(users.create_login_url(self.request.uri))

        

#On submission of form, actual registration

class authorize(webapp2.RequestHandler):
    def post(self):
        passes_allowed=3
        #key_n=db.Key(users.get_current_user().user_id())
        team=Team(key_name=users.get_current_user().user_id())
        team.member1=self.request.get('name1')
        team.member2=self.request.get('name2')
        team.score=0
        team.level=1
        team.daiict=self.request.get('daiict') != ''
        team.passes=passes_allowed
        team.uid=users.get_current_user().user_id()
        team.tname=self.request.get('team')
        team.email=users.get_current_user().email()
        regteam=self.request.get('team')
        team.put()
        self.redirect('/site/confirmation.html')

        



#Score Board

class scoreboard(webapp2.RequestHandler):
    def get(self):
        count=0
        teams=Team.all().order("-score").order("tstamp").fetch(10)
##        teams.order("-score")
##        teams.order("tstamp")
        team_list=[]
        for team in teams:
            
            if count>=10:
              break
            count=count+1
            team_list.append(team)
        template_values = {
            'team_list': team_list,
            
        }        
        
        template = jinja_environment.get_template('scoreboard.html')
        self.response.out.write(template.render(template_values))

class start(webapp2.RequestHandler):


  def get(self):
    #self.redirect('/site/notstarted.html')

    self.redirect('/site/timeover.html')

    #If not registered, send back to registration page.
    
    user=users.get_current_user()
    
    if user:
      teams=Team.all().filter('uid =',user.user_id())
    
      
      if teams.count()==0:
        #not registered, send to the registration page.
         self.redirect('/register')
      else:

        
        for t in teams:
          team=t
        present_level=team.level
        
        #self.response.out.write('''<p> question is ''' + questions[present_level])
        totalquestions=21;
        #if questions over
        if present_level==totalquestions:
          self.redirect('/site/gameover.html')

        
        passes_left=team.passes
        pass_text="Skip(%s)" %passes_left
        present_score=team.score
        ad="https://dl.dropbox.com/u/51976633/bj/bj%s.jpg" %(present_level-1)
        global questions,answers,images
        images="https://dl.dropbox.com/u/51976633/phase2/%s.jpg" %image[present_level]
        template_values = {
            'question': questions[present_level],
            'passes_left': passes_left,
            'image': images,
            'pass_text': pass_text,
            'score': present_score,
            'ad':ad,
            
        }        
        
        template = jinja_environment.get_template('start.html')
        self.response.out.write(template.render(template_values))
        




        
        #normal page comes here
    else:
      #google log in required.
      self.redirect(users.create_login_url(self.request.uri))

  def post(self):
    
    user=users.get_current_user()
    teams=Team.all().filter('uid =',user.user_id())
    for t in teams:
      team=t
    present_level=team.level
    
    global questions,answers,images
    submit=self.request.get('submit')
    pass_key=self.request.get('pass')
    if submit:
      answered=str(self.request.get('answer'))
      if answered==str(answers[present_level]):
        team.score=team.score+10
        team.level=team.level+1
        #set timestamp here
        team.tstamp=datetime.datetime.now()
        team.put()
        time.sleep(1.5)
        self.redirect('/start')
        
      else:
        self.get()
    elif pass_key:
      if team.passes<=0:
        team.level=team.level-1
        team.passes=team.passes+1
      team.passes=team.passes-1
      team.level=team.level+1
      #set timestamp here
      team.tstamp=datetime.datetime.now()
      team.put()
      time.sleep(1.5)
      self.redirect('/start')

class admin(webapp2.RequestHandler):
  def get(self):
        count1=0
        count2=0
        teams=Team.all()
        for team in teams:
          self.response.out.write(str(team.email)+'<br>')
        registered=teams.count()
        teams.order("-score")
        teams.order("tstamp")
        outside=Team.all()
        outside.order("-score")
        outside.order("tstamp")
        da_team_list=[]
        teams.filter("daiict =",True)
        outside.filter("daiict =",False)
        out_team_list=[]
        for team in teams:
            
            if count1>=40:
              break
            da_team_list.append(team)
##            self.response.out.write(str(count1)+'<br>')
            self.response.out.write(team.tname)
            self.response.out.write(team.member1)
            self.response.out.write('<br>')
##            self.response.out.write(team.score)
##            self.response.out.write('<br>')
            self.response.out.write(team.email+'<br>')
##            self.response.out.write('<br><hr>')
            count1=count1+1

        self.response.out.write('<b>Outside </b> <br>')
        for team in outside:
          if count2>=100:
            break
##          self.response.out.write(str(count2)+'<br>')
          out_team_list.append(team)
##          self.response.out.write(team.tname)
          self.response.out.write('<br>')
          self.response.out.write(team.email+',')
##          self.response.out.write('<br>')
##          self.response.out.write(team.score)
##          self.response.out.write('<br>')
          count2=count2+1

        self.response.out.write('<br> Registered users= ' + str(registered))


class trial(webapp2.RequestHandler):
  def get(self):
    ckey='VhqkWyz-f-RP9YYY2ZcOQUFBGPDLQix-'
    vkey='NmWb2NZuPdaGuYMM9GE3N4pl309f0OTI'
    hkey='-FecKRPhAvi42lJ7D3kijR.TSmLKi7rM'
    
    a = libsolvemedia.SolveMedia(ckey, vkey, hkey)
    self.response.out.write(a.get_html())
##    t = a.check_answer(libsolvemedia.remoteip, libsolvemedia.challenge, libsolvemedia.response)
##    if t['is_valid']:
##      self.response.out.write('harsh')
##    else:
##      self.response.out.write('nisar')
	
      
    
      
            

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', Register),
    ('/sign', authorize),
    ('/scoreboard', scoreboard),
    ('/start',start),
    ('/admin',admin),
    ('/trial',trial),
    
], debug=True)



