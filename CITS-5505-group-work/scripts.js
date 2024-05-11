$(document).ready(function(){
    $("#search-button").click(function(){
        var query = $("#search-input").val();
        
        // 用于存储所有接口的搜索结果
        var combinedResults = '';

        // 第一个接口的请求
        $.ajax({
            url: "/search_task",
            type: "GET",
            data: {query: query},
            success: function(taskResponse){
                // 处理任务搜索结果
                // 将任务搜索结果添加到 combinedResults 中
                combinedResults += taskResponse;
            }
        });

        // 第二个接口的请求
        $.ajax({
            url: "/search_user",
            type: "GET",
            data: {query: query},
            success: function(userResponse){
                // 处理用户搜索结果
                // 将用户搜索结果添加到 combinedResults 中
                combinedResults += userResponse;
            }
        });

        // 第三个接口的请求
        $.ajax({
            url: "/search_other",
            type: "GET",
            data: {query: query},
            success: function(otherResponse){
                // 处理第三个接口的搜索结果
                // 将第三个接口的搜索结果添加到 combinedResults 中
                combinedResults += otherResponse;

                // 显示合并后的搜索结果
                $("#search-results").html(combinedResults);

                // 显示模态框
                $('#searchModal').modal('show');
            }
        });
    });
});

//page4//
$(document).ready(function(){
    // 使用 AJAX 获取任务分类数据
    $.ajax({
        url: "/task_category",
        type: "GET",
        success: function(response){
            // 处理任务分类数据
            var categories = response.categories;
            
            // 遍历每个分类
            categories.forEach(function(category, index) {
                // 获取当前分类的第一个任务数据
                $.ajax({
                    url: "/task_category/" + category.id + "/first_task",
                    type: "GET",
                    success: function(task){
                        // 更新页面中当前分类的图像和文本
                        var imageBoxId = '';
                        switch (index) {
                            case 0:
                                imageBoxId = 'housing-task';
                                break;
                            case 1:
                                imageBoxId = 'transportation-task';
                                break;
                            case 2:
                                imageBoxId = 'entertainment-task';
                                break;
                            default:
                                break;
                        }
                        $("#" + imageBoxId).html('<img src="' + task.image_url + '" alt="' + category.name + '" class="img-fluid"><div class="text-box"><h2>' + category.name + '</h2></div>');
                    }
                });
            });
        }
    });
});

//page5//
$(document).ready(function(){
    // 使用 AJAX 获取前十个用户数据
    $.ajax({
        url: "/top_users",
        type: "GET",
        success: function(users){
            // 将用户数据填充到表格中
            var topUsersTable = '';
            users.forEach(function(user, index) {
                topUsersTable += '<tr><td>' + (index + 1) + '</td><td>' + user.username + '</td></tr>';
            });
            $("#top-users-chart").html('<table class="table"><thead><tr><th>Rank</th><th>Username</th></tr></thead><tbody>' + topUsersTable + '</tbody></table>');
        }
    });

    // 使用 AJAX 获取发布任务总数
    $.ajax({
        url: "/total_tasks",
        type: "GET",
        success: function(totalTasks){
            // 在 Total Tasks 栏中显示总任务数
            $("#total-tasks-chart").html('<h3 class="text-center">' + totalTasks + '</h3>');
        }
    });

    // 使用 AJAX 获取全部任务类型数据
    $.ajax({
        url: "/task_types",
        type: "GET",
        success: function(taskTypes){
            // 将任务类型数据填充到环形图表中
            var taskTypesData = [];
            var taskTypesLabels = [];
            taskTypes.forEach(function(taskType) {
                taskTypesData.push(taskType.count);
                taskTypesLabels.push(taskType.type);
            });
            var taskTypesChart = new Chart(document.getElementById('task-types-chart'), {
                type: 'pie',
                data: {
                    labels: taskTypesLabels,
                    datasets: [{
                        data: taskTypesData,
                        backgroundColor: ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8']
                    }]
                },
                options: {
                    responsive: true
                }
            });
        }
    });
});