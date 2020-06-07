from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import sqlite3
import os

class GetTodaysTask(Action):
    
    def name(self):
        return "get_todays_task"
    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        
        user_task = tracker.get_slot('date')
        user_task = int(user_task)
        conn = sqlite3.connect('tasks.sqlite')
        c = conn.cursor()
        c.execute("SELECT task FROM tasks_db WHERE date = {}".format(user_task))
        results = c.fetchall()
        conn.commit()
        conn.close()
        response = "Your today's task:\n{}".format(results)
        
        dispatcher.utter_message(response)
        return [SlotSet("time", results)]
    
class Completed(Action):
    
    def name(self):
        return "get_complete"
    def run(self, dispatcher, tracker, domain):
        user_task = tracker.get_slot('time')
        user_comp = tracker.get_slot('finish')
        conn = sqlite3.connect('tasks.sqlite')
        c = conn.cursor()
        if user_comp == 'Yes':
            c.execute('UPDATE tasks_db SET done = "Yes" WHERE date = {}'.format(user_task))
            response = "Ok then, have a nice day!"
            conn.commit()
            conn.close()
            dispatcher.utter_message(response)
        elif user_comp == 'No':
            c.execute('UPDATE tasks_db SET done = "No" WHERE date = {}'.format(user_task))
            response = "Which of them could'nt you complete?"
            conn.commit()
            conn.close()
            dispatcher.utter_message(response)
        
        return [SlotSet("finish", user_comp)]
    
class AddtoNext(Action):
    def name(self):
        return "add_to_next_day"
    
    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        user_task = tracker.get_slot('date')
        if user_task != '31':
            user_task = int(user_task) + 1
        else:
            user_task = int(user_task)
        conn = sqlite3.connect('tasks.sqlite')
        c = conn.cursor()
        subscribe = tracker.get_slot('add_task')
        task1 = tracker.get_slot('task_get')
        if subscribe == 'Yes':
            c.execute("SELECT day FROM tasks_db WHERE date = {}".format(user_task))
            day1 = c.fetchall()
            c.execute('INSERT INTO tasks_db'\
                      ' (date, day , task) VALUES'\
                      ' (?, ?, ?, ?)', (user_task, day1, task1))
            conn.commit()
            conn.close()
            dispatcher.utter_message("Your task has been added sucessfully")
        else:
            
            dispatcher.utter_message("Okay I won't")
        return [SlotSet("add_task", subscribe)]