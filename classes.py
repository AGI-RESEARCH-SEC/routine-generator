from copy import deepcopy, copy
from typing import Any

class TimeRange:
    '''
        start_time is time in minutes (to simplify time calculations)
        example: 6:10 o clock = (6*60 minutes) + (10 minutes)

        functions:
            substract
            time1.contains(time2)
    '''

    def __init__(self, start_time, stop_time):
        if type(start_time) == int:
            self.start_time = start_time
        else:
            self.start_time = int(start_time.split(':')[0]) * 60 + int(start_time.split(':')[1])
        if type(stop_time) == int:
            self.stop_time = stop_time
        else:
            self.stop_time = int(stop_time.split(':')[0]) * 60 + int(stop_time.split(':')[1])
    
    def contains(self, time1):
        # check if time1 lies within self
        
        if self.start_time <= time1.start_time and self.stop_time >= time1.stop_time:
            return True
        return False
    
    def __str__(self) -> str:
        return f'{self.start_time//60:02d}:{self.start_time%60:02d} - {self.stop_time//60:02d}:{self.stop_time%60:02d}'
    
    def __copy__(self):
        return TimeRange(self.start_time, self.stop_time)

    def __deepcopy__(self, memo):
        return TimeRange(deepcopy(self.start_time, memo), deepcopy(self.stop_time, memo))

class Students:
    # available_time = TimeRange       # 
    # preferred_time = TimeRange       #

    def __init__(self, batch='076BEI', room='000'):
        self.batch = batch      # Batch of the students
        self.room = room
    def __str__(self) -> str:
        return f'{self.batch} in room {self.room}'

class Subject:
    '''
        Subject has: Teacher, Students, time_left

        time_left (hrs.) is the time required to complete the syllabus
    '''
    
    def __init__(self, subject_name, students, time_left):
        self.subject_name = subject_name
        self.students = students
        self.time_left = time_left
    def __str__(self) -> str:
        return f'{self.subject_name} by {self.students.batch} at {self.time_left}'

class Teacher:
    '''
    
    available_time = TimeRange
    feasible_time = TimeRange
    subjects = []
    
    '''

    def __init__(self, teachers_name, subjects, feasible_time):
        self.name = teachers_name
        self.subjects = subjects
        self.feasible_time  = feasible_time
    def __str__(self) -> str:
        return f'{self.name} teaches {self.subjects} at {self.feasible_time}'
    
class ClassRoom:
    '''
        ClassRoom has: Students, Teacher, Subject, TimeRange, RoomNumber
    '''
    def __init__(self, teacher, subject, time, room_number='000'):
        # self.students = students
        self.teacher = teacher
        self.subject = subject
        self.time = time
        self.room_number = room_number
    
    def __str__(self) -> str:
        return f'{self.subject.subject_name} by {self.teacher.name} at {self.time}'
    
    @staticmethod
    def get_classes():
        # inputs:
        MIN_DURATION_PER_PEROID = 50    # 50 minutes per period
        rooms = ['102', '103']
        subjects = [Subject('AI', Students('bei076'), time_left=10), Subject('Data Mining', Students('bei076'), time_left=10)]
        teachers = [Teacher('teacher1', [subjects[0]], TimeRange('6:00', '10:00')), Teacher('teacher2', [subjects[1]], TimeRange('6:00', '10:00'))]
        COLLEGE_HOURS = TimeRange('6:00', '18:00')


        # All possible ClassRooms
        def segment_time(time_range, duration_of_each_segment):
            print(f'start : {time_range.start_time}, stop: {time_range.stop_time}, duration: {duration_of_each_segment}')
            time_slots = []
            while time_range.start_time < time_range.stop_time:
                time_slots.append(TimeRange(time_range.start_time, time_range.start_time + duration_of_each_segment))
                time_range.start_time += duration_of_each_segment
            # print(time_slots)
            return time_slots

        # time_slots = segment_time(TimeRange('6:10', '10:15'), 50)
        # print(f'time_slots: {[str(time) for time in time_slots]}')

        classrooms = []
        for teacher in teachers:
            time_slots = segment_time(deepcopy(teacher.feasible_time), MIN_DURATION_PER_PEROID)
            for each_time_slot in time_slots:
                for subject in teacher.subjects:
                    classrooms.append(ClassRoom(teacher, subject, each_time_slot))
            print(f'time_slots: {[str(time) for time in segment_time(teacher.feasible_time, MIN_DURATION_PER_PEROID)]}')

        # list of individual classes
        print(len(classrooms))
        return classrooms
    
    @staticmethod
    def get_inputs():
        subjects = [Subject('AI', Students('bei076'), time_left=10), Subject('Data Mining', Students('bei076'), time_left=10)]
        return {
        "MIN_DURATION_PER_PEROID" : 50,    # 50 minutes per period
        "rooms" : ['102', '103'],
        "subjects" : subjects,
        "teachers" : [Teacher('teacher1', [subjects[0]], TimeRange('6:00', '10:00')), Teacher('teacher2', [subjects[1]], TimeRange('6:00', '10:00'))],
        "COLLEGE_HOURS" : TimeRange('6:00', '18:00')
        }
    
    @staticmethod
    def is_valid(routine):
        # I. check if one teacher has more than one subject at a time
        subjects_by_teachers = {}
        for subjects in routine:
            for subject in subjects:
                for previous_subject_in_same_day in subjects_by_teachers:
                    if previous_subject_in_same_day.time.conflicts(subject.time):
                        return False, "Teacher has conflicting times:" + str(subject) + " and " + str(previous_subject_in_same_day)
                    else:
                        if subject.teacher.name not in subjects_by_teachers:
                            subjects_by_teachers[subject.teacher.name] = []
                        subjects_by_teachers[subject.teacher.name].append(subject)
                        
        # II. check conflicting time for student
        subjects_by_batchs = {}
        for subjects in routine:
            for subject in subjects:
                for previous_subject_in_same_day in subjects_by_batchs:
                    if previous_subject_in_same_day.time.conflicts(subject.time):
                        return False, "Student has conflicting times:" + str(subject) + " and " + str(previous_subject_in_same_day)
                    else:
                        if subject.students.batch not in subjects_by_batchs:
                            subjects_by_batchs[subject.students.batch] = []
                        subjects_by_batchs[subject.students.batch].append(subject)

        # III. check if subjects time lies within (feasible time of the teacher, college hours, special subject time)
        teachers = []
        for subjects in routine:
            for subject in subjects:
                # check for teachers feasible time
                if not subject.teacher.feasible_time.contains(subject.time):
                    return False, f"Teacher's feasible time does not contain subject time: \n teacher: {str(subject.teacher)} \n subject: {subject}"
                
                # check for college hours
                if not ClassRoom.get_inputs()["COLLEGE_HOURS"].contains(subject.time):
                    return False, f"College hours does not contain subject time: \n college hours: {str(ClassRoom.get_inputs()["COLLEGE_HOURS"])} \n subject: {subject}"
                
                # check if subject satisfies special subject time
                if subject.special_time is not None and not subject.special_time.contains(subject.time):
                    return False, f"Special subject time does not contain subject time: \n special time: {str(subject.special_time)} \n subject: {subject}"
        
        return True, "Valid Routine"