from django.db import models


# Create your models here.
class Freelancer(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    skills = models.CharField(max_length=200)

    def __str__(self):
        text = "Freelancer name: " + str(self.fullname) + "\nemail: " + str(self.email) + "\nskills: "\
               + str(self.skills) + "id: " + str(self.pk)
        return text


class Employer(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    # projects = models.ManyToOneRel.one_to_many(Project)

    def __str__(self):
        text = "Employer name: " + str(self.fullname) + "\nemail: " + str(self.email)
        return text


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    salary = models.FloatField()
    owner = models.ForeignKey(Employer, on_delete=models.CASCADE)

    def __str__(self):
        text = "Project name: " + str(self.name) + "\nDescription: " + str(self.description)\
                                + "\nSalary: " + str(self.salary) + "Ft\nOwner:\n" + str(self.owner)
        return text
