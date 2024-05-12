# 三个页面共同部分 jinjia2:
## class="top-bar" 涉及search功能，Rebecca 那边也涉及这个功能：

### 目前没有一个跳转的search页面，只使用了模态框展示搜索结果。不确定是否需要新建页面？
（也不确定我写的对不对）

```bash
<!-- Start of form -->
<form action="{{ url_for('search') }}" method="GET" class="search d-flex align-items-center">
    <img src="/static/search_icon.png" alt="Search Icon" style="width: 20px; height: 20px; margin-right: 10px;">
    <input type="text" name="query" placeholder="Search..." class="search-box">
    <button type="submit" class="button">Search</button>
</form>
<!-- End of form -->


<div id="searchModal" style="display:none;">
    <div class="modal-content">
        <span class="close">&times;</span>
        <div id="searchResults"></div>
    </div>
</div>



$('#searchForm').on('submit', function(e) {
        e.preventDefault();
        var query = $('.search-box').val();
        fetch(`/search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                var modal = $('#searchModal');
                var resultsContainer = $('#searchResults');
                resultsContainer.html('');

                if (data.error) {
                    resultsContainer.html('<p>' + data.error + '</p>');
                } else {
                    data.forEach(item => {
                        var resultElement = $('<div></div>');
                        resultElement.text(item.type + ': ' + item.title + ' - ' + item.content);
                        resultsContainer.append(resultElement);
                    });
                }
                modal.show();
            });

        $('.close').on('click', function() {
            $('#searchModal').hide();
        });
    });
```

<!-- ## side bar跳转链接的url_for写法，目前本地跳转不了，正常吗？
### 似乎后端要改route吗？？ -->




# profile.html 文件jinjia2 相关：

## 1. 密码重置
### 问题：点击submit目前不关闭窗口，可能是需要运行起来再测试这一点？？

```bash
{% if current_user.is_authenticated %}
    <div id="change-password-form" style="display: none;">
        <h2>Change Password</h2>
        <form id="passwordForm">
            <label for="old-password">Old Password:</label><br>
            <input type="password" id="old-password" name="old-password" required><br>
            <label for="new-password">New Password:</label><br>
            <input type="password" id="new-password" name="new-password" required><br>
    
            <button type="button" id="cancel-change-password-button">Cancel</button>
            <button type="submit" id="submit-change-password-button">Submit</button>
        </form>
    </div>
    {% endif %}



    $('#passwordForm').on('submit', function (e) {
    e.preventDefault();
    var current_password = $('#old-password').val();
    var new_password = $('#new-password').val();

        $.ajax({
            url: '/user/change_password',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                current_password: current_password,
                new_password: new_password
            }),
            success: function (response) {
                $('#successMessage').text('Password changed successfully').removeClass('hidden');
                $('#errorMessage').addClass('hidden');
                $('#old-password, #new-password').val('');
            },
            error: function (xhr) {
                $('#errorMessage').text('Error changing password: ' + xhr.responseJSON.error).removeClass('hidden');
                $('#successMessage').addClass('hidden');
            }
        });
    });
```

## 2. 个人信息的具体数据内容

### 目前mine.html中没有 user.location/user.university

```bash
<div id="edit-form" style="display: none;">
        <h2>Edit Profile</h2>
        <form>
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" value="{{ user.username }}"><br>
            <label for="age">Age:</label><br>
            <input type="text" id="age" name="age" value="{{ user.age }}"><br>
            <label for="gender">Gender:</label><br>
            <input type="text" id="gender" name="gender" value="{{ user.gender }}"><br>
            <label for="location">Location:</label><br>
            <input type="text" id="location" name="location" value="{{ user.location }}"><br>
            <label for="university">University:</label><br>
            <input type="text" id="university" name="university" value="{{ user.university }}"><br>
            <label for="avatar">Avatar:</label><br>
            <input type="file" id="avatar" name="avatar" accept="image/*"><br>
            # 不确定头像这部分的jinjia2:
            <img id="avatar-preview" src="{{ url_for('static', filename='uploads/' + user.avatar if user.avatar else 'uploads/default_avatar.png') }}" alt="Avatar preview"><br>

            <button type="button" id="cancel-button">Cancel</button>
            <button type="submit" id="submit-button">Submit</button>
        </form>
    </div>
```

## 3. 用户发布任务数、接受任务数、用户在全部用户中的排名

### 目前我在task 以及 user 下的view.py 中没找到相关的函数

但user 下的view.py中有相关的函数，我不确定怎么改，以及是不是应该转移到task/view.py??

```bash
@user.route('/<int:id>/tasks')
@login_required
def my_tasks(id):
    """Retrieve and display tasks posted by the current logged-in user."""
    try:
        user_id = id
        tasks = Task.query.filter_by(user_id=user_id).all()
        return render_template('mytask.html', tasks=tasks, current_user=current_user)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('task.index_page'))

```
## 4. 展示该用户由新到旧的发布/接受 任务的task title 以及 task detail

### 接收 或 发布 的任务怎么区分？后端是否有接口？
### 需要以由新到旧的顺序展示


```bash
{% if tasks %}
                    {% for task in tasks %}
                        <div class="row task-history">
                            <div class="col-md-12">
                                <div class="info-bar mb-3">
                                    <div class="info" id="task-info">
                                        <p class="task-title">{{ task.title }}</p>
                                    </div>
                                    <div class="task-detail" style="display: block;">
                                        <p>{{ task.content|safe }}</p> 
                                        <button class="button" onclick="toggleTaskDetail(this)">Read More</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                {% else %}
                    <div class="col-md-12">
                        <p>You have no task yet.</p>
                    </div>
                {% endif %}
```




# post.html
暂时似乎没什么···


# accept_task.html
## expected time是否有接口？（非task创建时间）


```bash
<div class="modal-body">
                <div id="taskDetails">
                    <p id="taskTitle">{{ task.title }}</p>
                    <p id="taskDetail"></p>
                    <div class="task-detail" style="display: block;">
                        <p>{{ task.content|safe }}</p> 
                    </div>
                    <p id="taskWhen">{{ task.expectedtime.strftime('%Y-%m-%d') }}</p>
                    <!-- and flexible ? -->

                    {% if task.img %}
                    <img id="taskPhoto" 
                    src="{{ task.get_img_url }}" 
                    alt="task photo" 
                    srcset="{{ task.get_img_url }} 1x, {{ task.get_img_url_hd }} 2x, {{ task.get_img_url_full_hd }} 3x">
                    {% endif %}

                </div>

                <form id="answerForm">
                    <div class="mb-3">
                        <label for="answer" class="form-label">Your Reply:</label>
                        <textarea class="form-control" id="answer" rows="3"></textarea>
                    </div>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Accept Task</button>
                </form>
            </div>
```









