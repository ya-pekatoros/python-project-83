data1 = """<html><head><title>The Dormouse's story</title></head>
<body>
<meta content="Test data #1" name="description">
<h1><span>Test</span> data #1</h1>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
</body>
</html>
"""

expectation1 = {"title": "The Dormouse's story", "h1": "<span>Test</span> data #1", "description": "Test data #1"}

data2 = """<html><head></head>
<body>
<meta content="Test data #1" name="description">
<h1>Test data #1</h1>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
</body>
</html>
"""

expectation2 = {"title": None, "h1": "Test data #1", "description": "Test data #1"}

data3 = """<html><head><title>The Dormouse's story</title></head>
<body>
<meta name="description">
<h1>Test data #1</h1>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
</body>
</html>
"""

expectation3 = {"title": "The Dormouse's story", "h1": "Test data #1", "description": None}

data4 = """<html><head><title>The Dormouse's story</title></head>
<body>
<h1>Test data #1</h1>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
</body>
</html>
"""

expectation4 = {"title": "The Dormouse's story", "h1": "Test data #1", "description": None}

data5 = """<html><head><title>The Dormouse's story</title></head>
<body>
<meta content="Test data #1">
<h1>Test data #1</h1>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
</body>
</html>
"""

expectation5 = {"title": "The Dormouse's story", "h1": "Test data #1", "description": None}

data6 = """<html><head><title>The Dormouse's story</title></head>
<body>
<meta content="Test data #1" name="description">
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
</body>
</html>
"""

expectation6 = {"title": "The Dormouse's story", "h1": None, "description": "Test data #1"}

data7 = """<html><head><title>The Dormouse's story</title></head>
<body>
<meta content="11111111" name="description">
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
</body>
</html>
"""

expectation7 = {
    "title": "The Dormouse's story",
    "h1": None,
    "description": "11111111"
}

test_data = [
    (data1, expectation1), (data2, expectation2), (data3, expectation3),
    (data4, expectation4), (data5, expectation5), (data6, expectation6),
    (data7, expectation7)
]
