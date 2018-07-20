from __future__ import unicode_literals
from django.db import models





class UserManager(models.Manager):


	def checkEmptyFields(self, request, **kwarg):
		for value in kwarg.values():
			if len(value) < 1:
				messages.info(request, "All fields are required", extra_tags="gen")
				return False
		return True

	def checkName(self, request):
		if len(request.POST['firstname']) < 2:
			messages.info(request, "First name must be at least 2 letters", extra_tags="fn")
		elif not request.POST['firstname'].isalpha():
			messages.info(request, "First name can only contain letters", extra_tags="fn")
		if len(request.POST['lastname']) < 2:
			messages.info(request, "Last name must be at least 2 letters", extra_tags="ln")
		elif not request.POST['lastname'].isalpha():
			messages.info(request, "Last name can only contain letters", extra_tags="ln")

	def checkEmail(self, request):
		if not EMAIL_REGEX.match(request.POST['email']):
			messages.info(request, "Wrong email format", extra_tags="em")

	def checkPassword(self, request):
		if len(request.POST['password1']) < 8:
			messages.info(request, "Password must be longer than 8 letters", extra_tags="pw1")
		if request.POST['password2'] != request.POST['password1']:
			messages.info(request, "Must have matching passwords", extra_tags="pw2")

	


	def add(self, request, level):
		if self.checkEmptyFields(request,					# check for empty fields on request.POST
				fn=request.POST['firstname'],
				ln=request.POST['lastname'],
				em=request.POST['email'],
				pw1=request.POST['password1'],
				pw2=request.POST['password2'] ):
			self.checkName(request)						# check for names' length and alpha
			self.checkEmail(request)					# check for email format
			self.checkPassword(request)					# chck for password length and match
			try:											# check existance in record
				User.objects.get(email=request.POST['email'])
				messages.info(request, "Provided email already exists in our record", extra_tags="gen")
			except ObjectDoesNotExist:
				pass # do nothing if record doens't exist, which is good

		if len(messages.get_messages(request)) > 0:
			return False

		else:
			hashed = request.POST['password1']
			User.objects.create(	first_name=request.POST['firstname'],
									last_name=request.POST['lastname'],
									email=request.POST['email'],
									hashedpw=hashed,
									description="",
									user_level=level) # need to hash later
			return True

	def register(self, request):
		if self.add(request, 9):
			user = User.objects.latest('created_at')
			request.session['id'] = user.id
			request.session['first_name'] = user.first_name
			request.session['last_name'] = user.last_name
			request.session['user_level'] = user.user_level
			return True
		else:
			return False

	def newuser(self, request):
		return self.add(request, 1)

	def login(self, request):
		user = None
		if self.checkEmptyFields(request,					# check for empty fields on request.POST
				em=request.POST['email'],
				pw1=request.POST['password']):

			try:
				user = User.objects.get(email=request.POST['email'])
				hashed = request.POST['password']

			except ObjectDoesNotExist:
				messages.info(request, "Provided email does not exist in our record", extra_tags="gen")

		if len(messages.get_messages(request)) > 0:
			return False
		else:
			request.session['id'] = user.id
			request.session['first_name'] = user.first_name
			request.session['last_name'] = user.last_name
			request.session['user_level'] = user.user_level
			return True

	def logoff(self, request):
		try:
			del request.session['id']
			del request.session['first_name']
			del request.session['last_name']
			del request.session['user_level']
		except KeyError:
			pass

	def getAllUsers(self):
		users = User.objects.all()
		return users

	def getOneUser(self, id):
		user = User.objects.get(id=id)
		return user

	def editInfo(self, request):
		if self.checkEmptyFields(request,					# check for empty fields on request.POST
				fn=request.POST['firstname'],
				ln=request.POST['lastname'],
				em=request.POST['userlevel']):
			self.checkName(request)						# check for names' length and alpha

		if len(messages.get_messages(request)) > 0:
			return False

		else:
			user = User.objects.get(id=request.POST['userid'])
			user.first_name=request.POST['firstname']
			user.last_name=request.POST['lastname']
			user.user_level=request.POST['userlevel']
			user.save()
			return True

	def editPW(self, request):
		if self.checkEmptyFields(request,
				pw1=request.POST['password1'],
				pw2=request.POST['password2']):
			self.checkPassword(request)					# chck for password length and match
		if len(messages.get_messages(request)) > 0:
			return False
		else:
			hashed = request.POST['password1']
			user = User.objects.get(id=request.POST['userid'])
			user.hashedpw=hashed
			user.save()
			return True

	def editDesc(self, request):
		user = User.objects.get(id=request.POST['userid'])
		user.description=request.POST['description']
		user.save()
		return True

	def deleteUser(self, request, id):
		if request.session['user_level'] == 9:
			user = User.objects.get(id=id).delete()


class User(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	hashedpw = models.CharField(max_length=255)
	description = models.TextField(null=True)
	user_level = models.IntegerField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()
	userManager = UserManager()
