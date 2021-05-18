import re


class Subject:
    def __init__(self, subject_name: str, exam_mark: int, mark: int, semester_mark: int, sum_mark: int):
        if not re.fullmatch(r'[-\w" ]{3,62}', subject_name):
            raise ValueError("Subject name is not str or contains characters not from set {letters, -, space, \"}")
        self.__subject_name: str = subject_name

        if not isinstance(mark, int) and (-1 <= mark <= 0 or 2 <= mark <= 5):
            raise ValueError("Mark is not int or not in set{-1, 0, 2-5}")
        self.__mark: int = mark

        if not isinstance(exam_mark, int) and ((exam_mark == 0 and not 3 <= mark <= 5) or 24 <= exam_mark <= 40):
            raise ValueError("Exam mark is not int or not in set{0, 24-40}")
        self.__exam_mark: int = exam_mark

        if not isinstance(semester_mark, int) and 0 <= semester_mark <= 60:
            raise ValueError("Semester mark is not int or not in range [0; 60]")
        self.__semester_mark: int = semester_mark

        if not isinstance(sum_mark, int) and sum_mark == semester_mark + exam_mark:
            raise ValueError("Summary mark in not int or not equal semester mark + exam mark")
        self.__sum_mark: int = sum_mark

    @property
    def subject_name(self) -> str:
        return self.__subject_name

    @property
    def mark(self) -> int:
        return self.__mark

    @property
    def exam_mark(self) -> int:
        return self.__exam_mark

    @property
    def semester_mark(self) -> int:
        return self.__semester_mark

    @property
    def sum_mark(self) -> int:
        return self.__sum_mark

    def __eq__(self, other) -> bool:
        return self.subject_name == other.subject_name

    def __repr__(self) -> str:
        return f"Subject name = {self.subject_name}\n" \
               f"Mark = {self.mark}\n" \
               f"Exam + semester = sum: {self.exam_mark} + {self.semester_mark} = {self.sum_mark}"


class Student:
    def __init__(self, first_name: str, middle_name: str, second_name: str, group: str, number: str):
        self.__subjects: list[Subject] = []

        if not re.fullmatch(r"[-\w' ]{1,21}", first_name):
            raise ValueError("First name is not str or contains characters not from set {letters, -, space, '}")
        self.__first_name: str = first_name

        if not re.fullmatch(r"[-\w' ]{1,23}", second_name):
            raise ValueError("Second name is not str or contains characters not from set {letters, -, space, '}")
        self.__second_name: str = second_name

        if not re.fullmatch(r"[-\w' ]{1,28}", middle_name):
            raise ValueError("Middle name is not str or contains characters not from set {letters, -, space, '}")
        self.__middle_name: str = middle_name

        if not re.fullmatch(r"[-\d\w ]{1,4}", group):
            raise ValueError("Group is not str or contains characters not from set {letters, -, digits}")
        self.__group: str = group

        if not re.fullmatch(r"\d{8}", number):
            raise ValueError("Number is not str or contains not only digits")
        self.__number: str = number

    def load(self, subject_name: str, exam_mark: int, mark: int, semester_mark: int, sum_mark: int):
        pass

    @property
    def number(self) -> str:
        return self.__number

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def second_name(self) -> str:
        return self.__second_name

    @property
    def middle_name(self) -> str:
        return self.__middle_name

    @property
    def group(self) -> str:
        return self.__group

    def __eq__(self, other) -> bool:
        return self.number == other.number

    def __repr__(self) -> str:
        return f"Subjects = {self.__subjects}\n" \
               f"Name = {self.first_name} {self.middle_name} {self.second_name}\n" \
               f"Group = {self.group}\n" \
               f"Number = {self.number}"


class Info:
    def __init__(self):
        self.__students: list[Student] = []
        self.__total_cnt_write: int = 0
        self.__cnt_not_come: int = 0

    def clear(self):
        self.__students: list[Student] = []
        self.__total_cnt_write: int = 0
        self.__cnt_not_come: int = 0

    def output(self, output_name: str, encoding: str):
        pass

    def load(self, first_name: str, middle_name: str, second_name: str, group: str, number: str,
             subject_name: str, exam_mark: int, mark: int, semester_mark: int, sum_mark: int):
        student = self.find(number)
        if student is None:
            student = self.add(first_name, middle_name, second_name, group, number)

        student.load(subject_name, exam_mark, mark, semester_mark, sum_mark)

    def find(self, number: str) -> Student or None:
        for student in self.__students:
            if student.number == number:
                return student
        return None

    def add(self, first_name: str, middle_name: str, second_name: str, group: str, number: str) -> Student:
        self.__students.append(Student(first_name, middle_name, second_name, group, number))
        return self.__students[-1]

    @property
    def total_cnt_write(self) -> int:
        return self.__total_cnt_write

    @property
    def cnt_not_come(self) -> int:
        return self.__cnt_not_come

    def __repr__(self) -> str:
        return f"Students = {self.__students}\n" \
               f"Total count write = {self.total_cnt_write}\n" \
               f"Count not come = {self.cnt_not_come}"
