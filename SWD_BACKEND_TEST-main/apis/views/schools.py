from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.models import SchoolStructure, Schools, Classes, Personnel, Subjects, StudentSubjectsScore

class StudentSubjectsScoreAPIView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        # Extract data from request
        student_first_name = request.data.get("first_name", None)
        student_last_name = request.data.get("last_name", None)
        subject_title = request.data.get("subject_title", None)
        score_value = request.data.get("score", None)

        # Check if all required fields are present
        if None in [student_first_name, student_last_name, subject_title, score_value]:
            return Response({"message": "Payload data incomplete"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate types and values
        if not isinstance(student_first_name, str) or not isinstance(student_last_name, str) \
                or not isinstance(subject_title, str) or not isinstance(score_value, (int, float)):
            return Response({"message": "Invalid data types in payload"}, status=status.HTTP_400_BAD_REQUEST)

        if not (0 <= score_value <= 100):
            return Response({"message": "Score must be between 0 and 100"}, status=status.HTTP_400_BAD_REQUEST)

        # Find student and subject objects
        try:
            student = StudentSubjectsScore.student.objects.get(first_name=student_first_name, last_name=student_last_name)
            subject = StudentSubjectsScore.subjects.objects.get(title=subject_title)
        except StudentSubjectsScore.student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_400_BAD_REQUEST)
        except StudentSubjectsScore.subjects.DoesNotExist:
            return Response({"message": "Subject not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if score for this subject and student already exists
        try:
            score = StudentSubjectsScore.score.objects.get(student=student, subject=subject)
            # If exists, update the score
            score.score = score_value
            score.save()
            return Response({"message": "Score updated successfully",
                             "student_first_name": student.first_name,
                             "student_last_name": student.last_name,
                             "subject_title": subject.title,
                             "credit": score.credit,
                             "score": score.score}, status=status.HTTP_201_CREATED)
        except StudentSubjectsScore.score.DoesNotExist:
            # If not exists, create a new score
            score = StudentSubjectsScore.score.objects.create(student=student, subject=subject, score=score_value)
            return Response({"message": "Score created successfully",
                             "student_first_name": student.first_name,
                             "student_last_name": student.last_name,
                             "subject_title": subject.title,
                             "credit": score.credit,
                             "score": score.score}, status=status.HTTP_201_CREATED)


            


class StudentSubjectsScoreDetailsAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        student_id = kwargs.get("id")

        # Step 1: Retrieve student details from the database
        try:
            # Assuming student_id is the ID of the Personnel instance (student)
            student = Personnel.objects.get(id=student_id)
        except Personnel.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Retrieve subjects associated with the student
        subjects = StudentSubjectsScore.objects.filter(student=student)

        # Step 3: Calculate scores, grades, and grade point average for each subject
        subject_details = []
        total_credit = 0
        total_score = 0
        for subject in subjects:
            score = subject.score
            grade = calculate_grade(score)
            total_credit += subject.credit
            total_score += score * subject.credit
            subject_details.append({
                "subject": subject.subjects.title,
                "credit": subject.credit,
                "score": score,
                "grade": grade
            })

        # Calculate grade point average
        if total_credit > 0:
            gpa = total_score / total_credit
        else:
            gpa = 0

        # Step 4: Compile the data into the desired format
        context_data = {
            "student": {
                "id": student.id,
                "full_name": student.first_name + " " + student.last_name,
                "school": student.school_class.school.title
            },
            "subject_detail": subject_details,
            "grade_point_average": gpa
        }

        # Step 5: Return the data as a response
        return Response(context_data, status=status.HTTP_200_OK)


def calculate_grade(score):
    if score >= 80:
        return "A"
    elif 75 <= score < 80:
        return "B+"
    elif 70 <= score < 75:
        return "B"
    elif 65 <= score < 70:
        return "C+"
    elif 60 <= score < 65:
        return "C"
    elif 55 <= score < 60:
        return "D+"
    elif 50 <= score < 55:
        return "D"
    else:
        return "F"


class PersonnelDetailsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        school_title = kwargs.get("school_title", None)
        your_result = []

        try:
            # Get the school object based on the provided title
            school = Schools.objects.get(title=school_title)

            # Get all classes associated with the school
            classes = Classes.objects.filter(school=school)

            # Get personnel for all classes of the school
            personnel = Personnel.objects.filter(school_class__in=classes)

            # Sort personnel by role, class order, and last name
            personnel = personnel.order_by('personnel_type', 'school_class__class_order', 'last_name')

            # Prepare the response data
            for idx, person in enumerate(personnel, start=1):
                your_result.append(f"{idx}. school: {school.title}, role: {person.get_personnel_type_display()}, class: {person.school_class.class_order}, name: {person.first_name} {person.last_name}")

            return Response(your_result, status=status.HTTP_200_OK)
        except Schools.DoesNotExist:
            return Response({"message": "School not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SchoolHierarchyAPIView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        your_result = []

        try:
            # Get all schools
            schools = Schools.objects.all()

            # Iterate through each school
            for school in schools:
                school_data = {
                    "school": school.title,
                }

                # Get all classes for the current school
                classes = Classes.objects.filter(school=school)

                class_data = {}

                # Iterate through each class of the school
                for _class in classes:
                    class_teacher = Personnel.objects.filter(school_class=_class, personnel_type=0).first()
                    head_of_room = Personnel.objects.filter(school_class=_class, personnel_type=1).first()
                    students = Personnel.objects.filter(school_class=_class, personnel_type=2)

                    class_teacher_name = f"{class_teacher.first_name} {class_teacher.last_name}" if class_teacher else ""
                    head_of_room_name = f"{head_of_room.first_name} {head_of_room.last_name}" if head_of_room else ""

                    class_data[f"class {_class.class_order}"] = {
                        f"Teacher: {class_teacher_name}": None,
                        f"Head of the room": head_of_room_name,
                        "Students": [f"{student.first_name} {student.last_name}" for student in students]
                    }

                school_data.update(class_data)
                your_result.append(school_data)

            return Response(your_result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SchoolStructureAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        [Logical Test]

        description: get School's structure list in hierarchy.
        """

        def get_school_structure(data):
            result = []
            for item in data:
                node = {
                    "title": item["title"],
                    "sub": []
                }
                if "sub" in item:
                    node["sub"] = get_school_structure(item["sub"])
                result.append(node)
            return result

        # Fetching data from the database
        data_pattern = []

        schools = Schools.objects.all()

        for school in schools:
            school_data = {"title": school.title, "sub": []}
            classes = Classes.objects.filter(school=school)
            for _class in classes:
                class_data = {"title": f"ม.{_class.class_order}", "sub": []}
                school_data["sub"].append(class_data)
                students = Personnel.objects.filter(school_class=_class, personnel_type=2)
                for student in students:
                    class_data["sub"].append({"title": f"ห้อง {_class.class_order}/{student.id}"})

class SchoolStructureAPIView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        # Query all top-level structures (schools without parent)
        top_level_structures = SchoolStructure.objects.filter(parent=None)

        # Initialize the result list
        your_result = []

        # Iterate through each top-level structure
        for top_structure in top_level_structures:
            # Create a dictionary for the top-level structure
            top_structure_dict = {
                "title": top_structure.title,
                "sub": []
            }

            # Fetch sub-structures (classes) for the current top-level structure
            sub_structures = SchoolStructure.objects.filter(parent=top_structure)

            # Iterate through each sub-structure
            for sub_structure in sub_structures:
                # Create a dictionary for the sub-structure
                sub_structure_dict = {
                    "title": sub_structure.title,
                    "sub": []
                }

                # Fetch sub-sub-structures (classrooms) for the current sub-structure
                sub_sub_structures = SchoolStructure.objects.filter(parent=sub_structure)

                # Iterate through each sub-sub-structure (classroom)
                for sub_sub_structure in sub_sub_structures:
                    # Create a dictionary for the sub-sub-structure (classroom)
                    sub_sub_structure_dict = {
                        "title": sub_sub_structure.title
                    }

                    # Append the sub-sub-structure dictionary to the sub-structure's "sub" list
                    sub_structure_dict["sub"].append(sub_sub_structure_dict)

                # Append the sub-structure dictionary to the top-level structure's "sub" list
                top_structure_dict["sub"].append(sub_structure_dict)

            # Append the top-level structure dictionary to the result list
            your_result.append(top_structure_dict)

        # Return the result list as a response
        return Response(your_result, status=status.HTTP_200_OK)