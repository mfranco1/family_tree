import datetime

class Person:
	def __init__(self,f_name,l_name,gender,birth_date="unknown",father="",mother=""):
		self.f_name = f_name
		self.l_name = l_name
		self.gender = gender
		self.birth_date = birth_date
		self.father = father
		self.mother = mother
		self.death_date = ""
		self.spouse = ""
		self.children = []
		self.age = self.update_age()

	#### GETTERS ####

	def get_full_name(self):
		return self.f_name+" "+self.l_name

	def get_gender(self):
		return self.gender

	def get_birth_date(self):
		return self.birth_date

	def get_father(self):
		return self.father

	def get_mother(self):
		return self.mother

	def get_death_date(self):
		if self.is_dead():
			return self.death_date
		return "Still Alive"

	def get_spouse(self):
		if self.is_married():
			return self.spouse
		return "Not Married"

	def get_children(self):
		if self.has_children():
			return self.children
		return "Has No Children"

	def get_child(self,order=0):
		if self.has_children():
			return self.children[order]
		return "Has No Children"

	def get_age(self):
		return self.age

	#### SETTERS ####

	def set_birth_date(self,birth_date):
		self.birth_date = birth_date

	def set_father(self,father):
		self.father = father

	def set_mother(self,mother):
		self.mother = mother

	def set_death_date(self,death_date):
		self.death_date = death_date

	def set_spouse(self,spouse):
		self.spouse = spouse

	def add_child(self,child):
		if child:
			self.children.append(child)
			self.children.sort(key=lambda x: x.get_age(), reverse=True)

	def add_children(self,children):
		if children:
			for child in children:
				self.children.append(child)
			self.children.sort(key=lambda x: x.get_age(), reverse=True)

	def update_age(self):
		today = datetime.date.today()
		bdate = datetime.date(*(int(s) for s in self.birth_date.split('-')))
		self.age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
		print(self.get_full_name()+" "+str(self.age))

	#### CHECKERS ####

	def is_dead(self):
		if not self.death_date:
			return False
		return True

	def is_married(self):
		if not self.spouse:
			return False
		return True

	def has_children(self):
		if not self.children:
			return False
		return True


def make_person(f_name,l_name,gender,birth_date="unknown",father="",mother=""):
	return Person(f_name,l_name,gender,birth_date,father,mother)

def find_person(list,name):
	for p in list:
		if p:
			if name == p.get_full_name():
				return p
	return ""

def link_child_parent(person):
	if person:
		if person.get_father() and not isinstance(person.get_father(),str):
			person.get_father().add_child(person)
		if person.get_mother() and not isinstance(person.get_mother(),str):
			person.get_mother().add_child(person)

def link_parent_child(list,person):
	if not person:
		return ""
	for p in list:
		if p:
			if person.get_gender() == "Male" and p.get_father() == person.get_full_name():
				person.add_child(p)
			elif person.get_gender() == "Female" and p.get_mother() == person.get_full_name():
				person.add_child(p)

def link_spouse(list,person):
	if not person:
		return ""
	for p in list:
		if p:
			if isinstance(person.get_spouse(),str) and person.get_spouse() == p.get_full_name():
				person.set_spouse(p)
				p.set_spouse(person)
			elif isinstance(person.get_spouse(),Person) and person.get_spouse().get_full_name() == p.get_full_name():
				p.set_spouse(person)

def traverse_from(person,indent=0):
	if person:
		pad = "  "
		for i in range(indent):
			pad+=pad
		print("\n"+pad,end="",flush=True)
		print(person.get_full_name(),end="",flush=True)
		if person.is_married():
			if isinstance(person.get_spouse(),Person):
				print(" --- "+person.get_spouse().get_full_name())
			else:
				print(" --- "+person.get_spouse())
		if person.has_children():
			indent+=1
			for child in person.children:
				traverse_from(child,indent)

def traverse_all(person):
	if person:
		while person.father or person.mother:
			person = person.father
		traverse_from(person)