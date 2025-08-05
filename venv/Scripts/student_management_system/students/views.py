from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm, UserForm
from django.contrib.auth import login, authenticate

@login_required
def student_list(request):
    if not request.user.is_staff:
        return redirect('my_profile')
    
    students = Student.objects.select_related('user').all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def student_create(request):
    if not request.user.is_staff:
        return redirect('my_profile')

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('student_list')
    else:
        user_form = UserForm()
        student_form = StudentForm()

    context = {
        'user_form': user_form,
        'student_form': student_form,
        'title': 'Add Student',
        'button_label': 'Create'
    }
    return render(request, 'students/student_form.html', context)

@login_required
def student_update(request, pk):
    if not request.user.is_staff:
        return redirect('my_profile')

    student = get_object_or_404(Student, pk=pk)
    user = student.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            if password:
                user.set_password(password)
            user.save()
            student_form.save()
            return redirect('student_list')
    else:
        user_form = UserForm(instance=user)
        user_form.fields['password'].widget.attrs['placeholder'] = "Enter new password or leave blank"
        user_form.fields['password'].required = False
        student_form = StudentForm(instance=student)

    context = {
        'user_form': user_form,
        'student_form': student_form,
        'title': 'Edit Student',
        'button_label': 'Update'
    }
    return render(request, 'students/student_form.html', context)

@login_required
def student_delete(request, pk):
    if not request.user.is_staff:
        return redirect('my_profile')

    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        return redirect('student_list')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})

@login_required
def my_profile(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'students/my_profile.html', {'student': student})
