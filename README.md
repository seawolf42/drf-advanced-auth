# DRF Advanced Authentication

[Django REST Framework](https://www.django-rest-framework.org/) provides just about everything needed to turn your Django app into a REST-based web application. One area that DRF lacks functionality is in the non-happy path scenarios related to authentication, namely password changes and password resets. This module aims to simplify setting up a full auth subsystem for your REST application.

The functions provided by this package are:

-   login: an endpoint for authenticating a user
-   logout: an endpoint for ending a user's session
-   change password: an endpoint for changing the password of a logged-in user
-   reset password: two endpoints that together can be used to reset the password of a logged-out user (lost password, etc)

**Note:** This package is a work in progress (that's why it's not yet at version 1.0). I am active seeking contributions to help with making it more usable, see ["Contributing"](#contributing) below.

## Installation

Install the package:

```bash
$ pip install drf-advanced-auth
```

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'drf_advanced_auth',
    ...
]
```

Update your URLs by adding the `drf_advanced_auth` urls under whatever prefix you want, and another url named `password_reset_confirm` that you want users to be redirected to when they click the link in the password reset email:

```python
urlpatterns = [
    url(r'^auth/', include('drf_advanced_auth.urls', namespace='authentication')),
    url(r'^password-reset/update/(?P<uidb64>.*)/(?P<token>.*)', FakeView.as_view(), name='password_reset_confirm'),
]
```

## Usage

(IN PROGRESS)

## Sample App

You can see a sample app using these fields buy running the following:

```bash
$ python manage.py migrate
$ python manage.py loaddata fixtures/base.json
$ python manage.py runserver
```

This app has the following endpoints (assuming they are under the `auth` prefix as shown above):

-   `/auth/login/`
-   `/auth/logout/`
-   `/auth/change_password/`
-   `/auth/reset_password_request/`
-   `/auth/reset_password_complete/`

The username for the admin user is `admin`, and the password is `pass`.

<a name="contributing"></a>

## Contributing

I am actively seeking contributions to this package. Check the "Issues" section of the repository for my current hit list.

If you have suggestions for other features I am open to hearing them. Use the "Issues" section of the repository to start a conversation.
