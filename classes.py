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
    
    @staticmethod
    def segment_time(time_range, duration_of_each_segment):
            # All possible ClassRooms
            print(f'start : {time_range.start_time}, stop: {time_range.stop_time}, duration: {duration_of_each_segment}')
            time_slots = []
            while time_range.start_time < time_range.stop_time:
                time_slots.append(TimeRange(time_range.start_time, time_range.start_time + int(duration_of_each_segment)))
                time_range.start_time += int(duration_of_each_segment)
            # print(time_slots)
            return time_slots

        # time_slots = TimeRange.segment_time(TimeRange('6:10', '10:15'), 50)
        # print(f'time_slots: {[str(time) for time in time_slots]}')

    def __str__(self) -> str:
        return f'{self.start_time//60:02d}:{self.start_time%60:02d} - {self.stop_time//60:02d}:{self.stop_time%60:02d}'
    
    def __copy__(self):
        return TimeRange(self.start_time, self.stop_time)

    def __deepcopy__(self, memo):
        return TimeRange(deepcopy(self.start_time, memo), deepcopy(self.stop_time, memo))
    
    def __add__(self, value):
        print(type(self.start_time))
        return TimeRange(self.start_time, int(self.stop_time) + int(value))

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
    
    def __init__(self, subject_name, students, teacher, time_left=None, room_number='000', special_time=None):
        self.subject_name = subject_name
        self.students = students
        self.teacher = teacher
        self.time_left = time_left
        self.room_number = room_number
        self.special_time = special_time
        
    def __str__(self) -> str:
        return f'{self.subject_name} by {self.students.batch} at {self.time_left}'

class Teacher:
    '''
    
    available_time = TimeRange
    feasible_time = TimeRange
    subjects = []
    
    '''

    def __init__(self, teachers_name, feasible_time):
        self.name = teachers_name
        # self.subjects = subjects
        self.feasible_time  = feasible_time
    def __str__(self) -> str:
        return f'{self.name} teaches {self.subjects} at {self.feasible_time}'

class ClassRoomRoutine:
    def __init__(self, classes={}):
        self.classes = classes
    
    def add_class(self, class_room):
        print(class_room.subject.students)
        if class_room.subject.students not in self.classes:
            self.classes[class_room.subject.students] = [class_room]
        else:
            self.classes[class_room.subject.students].append(class_room)
    def get(self):
        return self.classes

class ClassRoom:
    '''
        ClassRoom has: Students, Teacher, Subject, TimeRange, RoomNumber
    '''
    def __init__(self, subject, time):
        # self.students = students
        # self.teacher = teacher
        self.subject = subject
        self.time = time
        # self.room_number = room_number
    
    def __str__(self) -> str:
        return f'{self.subject.subject_name} by {self.teacher.name} at {self.time}'
    
    @staticmethod
    def get_classes():
        # inputs:
        MIN_DURATION_PER_PEROID = 50    # 50 minutes per period
        rooms = ['102', '103']
        
        teachers = [Teacher('Baikuntha Acharya', TimeRange('6:00', '10:00')), Teacher('Bharat Bhatta', TimeRange('6:00', '10:00'))]
        subjects = [Subject('AI', Students('bei076'),teachers[0],  time_left=10), Subject('Data Mining', Students('bei076'), time_left=10)]
        
        COLLEGE_HOURS = TimeRange('6:00', '18:00')


        
        

        classrooms = []
        for teacher in teachers:
            time_slots = TimeRange.segment_time(deepcopy(teacher.feasible_time), MIN_DURATION_PER_PEROID)
            for each_time_slot in time_slots:
                for subject in teacher.subjects:
                    classrooms.append(ClassRoom(teacher, subject, each_time_slot))
            print(f'time_slots: {[str(time) for time in TimeRange.segment_time(teacher.feasible_time, MIN_DURATION_PER_PEROID)]}')

        # list of individual classes
        print(len(classrooms))
        return classrooms
    
    @staticmethod
    def get_inputs():
        teachers = [Teacher('Baikuntha Acharya', TimeRange('6:00', '10:00')), Teacher('Bharat Bhatta', TimeRange('6:00', '10:00'))]
        subjects = [Subject('AI', Students('bei076'), teachers[0],  time_left=10), Subject('Data Mining', Students('bei076'), teachers[1], time_left=10)]

        return {
        "MIN_DURATION_PER_PEROID" : 50,    # 50 minutes per period
        "rooms" : ['102', '103'],
        "all_subjects" : subjects,
        "all_teachers" : teachers,
        "COLLEGE_HOURS" : TimeRange('6:00', '18:00')
        }
    
    @staticmethod
    def is_valid(routine):
        # I. check if one teacher has more than one subject at a time
        subjects_by_teachers = {}
        print(routine.get())
        for students_batch in routine.get():
            for subject in routine.get()[students_batch]:
                for previous_subject_in_same_day in subjects_by_teachers:
                    if previous_subject_in_same_day.time.conflicts(subject.time):
                        return False, "Teacher has conflicting times:" + str(subject) + " and " + str(previous_subject_in_same_day)
                    else:
                        if subject.teacher.name not in subjects_by_teachers:
                            subjects_by_teachers[subject.teacher.name] = []
                        subjects_by_teachers[subject.teacher.name].append(subject)
        
        # II. check conflicting time for student
        subjects_by_batchs = {}
        for students_batch in routine.get():
            for subject in routine.get()[students_batch]:
                for previous_subject_in_same_day in subjects_by_batchs:
                    if previous_subject_in_same_day.time.conflicts(subject.time):
                        return False, "Student has conflicting times:" + str(subject) + " and " + str(previous_subject_in_same_day)
                    else:
                        if subject.students.batch not in subjects_by_batchs:
                            subjects_by_batchs[subject.students.batch] = []
                        subjects_by_batchs[subject.students.batch].append(subject)

        # III. check if subjects time lies within (feasible time of the teacher, college hours, special subject time)
        teachers = []
        for students_batch in routine.get():
            for classroom in routine.get()[students_batch]:
                # check for teachers feasible time
                if not classroom.subject.teacher.feasible_time.contains(classroom.time):
                    return False, f"Teacher's feasible time does not contain subject time: \n teacher: {str(classroom.subject.teacher)} \n subject: {classroom.subject}"
                
                # check for college hours
                if not ClassRoom.get_inputs()["COLLEGE_HOURS"].contains(classroom.time):
                    return False, f"College hours does not contain subject time: \n college hours: {str(ClassRoom.get_inputs()['COLLEGE_HOURS'])} \n subject: {classroom.subject}"
                
                # check if subject satisfies special subject time
                if classroom.subject.special_time is not None and not classroom.subject.special_time.contains(classroom.time):
                    return False, f"Special subject time does not contain subject time: \n special time: {str(classroom.subject.special_time)} \n subject: {classroom.subject}"
        
        return True, "Valid Routine"
    @staticmethod
    def get_available_subjects(all_subjects, time, Routine):
        routine_copy = deepcopy(Routine)
        available_subjects = all_subjects
        for subject in all_subjects:
            if subject.time_left > 0:
                
                # add subject to routine and check validity
                routine_second_copy = deepcopy(routine_copy)
                routine_second_copy.add_class(ClassRoom(subject, time))
                is_valid, msg = ClassRoom.is_valid(routine_second_copy)
                
                if is_valid:
                    routine_copy = routine_second_copy
                    available_subjects.append(subject)
                    

                '''
                * remove subject for which teacher is not available (not teachers feasible time, teacher already has a ClassRoom at that time)
                * remove sub for which student already has a ClassRoom at that time
                * remove sub for which subject time is not within college hours
                * remove sub for which subject time is not within special subject time
                '''
        return available_subjects
    @staticmethod
    def get_available_teachers(all_teachers, all_subjects, subject, time, Routine):
        available_teachers = all_teachers
        pre_occupied_teachers = []
        for batch in Routine:
            for subject in Routine[batch]:
                pre_occupied_teachers.append(subject.teacher)
        
        # teacher not pre-occupied and teacher feasible time contains subject time
        available_teachers = [teacher for teacher in available_teachers if (teacher not in pre_occupied_teachers and teacher.feasible_time.contains(time + '50'))]
        
        return available_teachers