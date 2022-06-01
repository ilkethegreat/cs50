# CS50 FINAL PROJECT: TODO
## Description:
    In my CS50 final project, I've created a web application using flask, html, css, python, jinja and sql. In my web simple web application, users can add their do-lists to the page so they won't forget them. The added daily tasks remain on the page as long as the user doesn't update or delete them, which allows users to come back with same tasks being there.
## Video:  <https://youtu.be/wofMDGdcW84>
---------------------------------------------------------------------------------------------------------------
### Python:
#### In app.py, the libraries that've been used are flask, flask-sqlalchemy, and datetime. From flask and flask-sqlalchemy I've imported Flask and render_template, request, and redirect as basic requirements. From datetime I've imported datetime so I can let the user know the date they've added the task. Then, I initialized Flask and SQLAlchemy in lines 4-6. I created a special class called dolist to pass necessary information in upcoming lines, then I created routes and respective functions for main page, update and delete.
---------------------------------------------------------------------------------------------------------------
### Static:
#### In static there's a CSS that only gives style to form in the page:
    form {
    align-items: center;
    text-align: center;
    flex: 1;
    height: 33px;
    font-size: 16px;
    padding-left: 5px; }
---------------------------------------------------------------------------------------------------------------
### Templates:
#### In templates, I have a base template called "base.html" that is the base of my other html templates. In that template, I've used html5 to leverage Bootstrap. In my <head> tag, I have linked the Bootstrap and my tiny style sheet. In the tag, there are also two classic meta tags and page title as well:
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>TODO</title>
#### To specify the header, it finishes with a basic jinja syntax (Same for the body page, except that block is called {% block body %}):
    {% block head %}{% endblock %}
#### In my "index.html" within the same folder, there's the header of my webpage's look statically:
    <h1 style="text-align:center; padding-bottom: 15px; padding-top:15px; background-color: rgb(23,23,23); color: rgb(200,200,200);">TODO</h1>
#### And there's an if jinja statement to show an additional header that notifies user that there're no tasks added for now if the task count is fewer than one:
    {% if tasks|length < 1 %}
    <h1 style="text-align:center; padding-bottom: 15px; padding-top:15px; font-size: 17px;">There are no tasks added for now. Add one below!</h1>
    {% else %}
    ---code---
    {% endif %}
#### In the ---code---, there is a table. That table contains <thead> and <tbody> tags. <thead> tag contains static columns called Task, Added, and Actions. Before <tbody> tag, there's an additional jinja syntax to pull data from python and stream it on the page:
        {% for task in tasks %}
        <tbody>
            <tr>
                <td>{{ task.content }}</td>
                <td>{{ task.dateCreated.date() }}</td>
                <td>
                    <a href="/delete/{{task.id}}">Delete</a>
                    <br>
                    <a href="/update/{{task.id}}">Update</a>
                </td>
            </tr>
         </tbody>
        {% endfor %}
#### I get the task content and time created from the user by creating a loop, and stream it on the webpage. Then, if the user wants to delete or update the task, I have the "a" tags for referring the data back to Python. One of which just deletes the task, as can been seen in Python:
    @app.route('/delete/<int:id>')
    def delete(id):
    taskDeleted = dolist.query.get_or_404(id)

    try:
        db.session.delete(taskDeleted)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting the task."
#### And the other refers to update.html and renders the template. In "update.html", there's a few lines of code to update the content (in this case the task) by the data passed in by the user:
    <div>
        <h1 style="text-align:center; padding-bottom: 15px; padding-top:15px;">Update Task</h1>

        <div>
            <form action="/update/{{task.id}}" method="POST">
                <input type="text" name="content" id="content" value="{{task.content}}">
                <input type="submit" value="Update">
            </form>
        </div>
    </div>

### And that was my final project TODO! Thanks for viewing! It was CS50!
-----------------------------------------------------------------------------------------------------------
<h1 style="text-align:center; padding-bottom: 15px; padding-top:15px; background-color: rgb(23,23,23); color: rgb(200,200,200);">TODO</h1>




