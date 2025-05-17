from app import app
from models.models import db, SkillTest

tests_data = {
    "python": [
        ("What does the 'len()' function do in Python?", ["Returns the length", "Returns max", "Deletes object", "Reverses list"], "Returns the length"),
        ("What is the output of: print(type([]))", ["list", "<class 'list'>", "[]", "type error"], "<class 'list'>"),
        ("What keyword is used for function in Python?", ["func", "def", "function", "lambda"], "def"),
        ("Which of these is not a core data type?", ["Tuples", "Lists", "Class", "Dictionary"], "Class"),
        ("How do you start a comment in Python?", ["//", "#", "/*", "--"], "#"),
        ("What does '==' check?", ["Assignment", "Equality", "Identity", "None"], "Equality"),
        ("What is the result of 2 ** 3?", ["6", "8", "9", "Error"], "8"),
        ("Which method is used to add item to list?", ["add()", "append()", "insert()", "push()"], "append()"),
        ("What does 'break' do in loop?", ["Skips iteration", "Exits loop", "Pauses loop", "Does nothing"], "Exits loop"),
        ("What is a correct syntax for dictionary?", ["{key:value}", "[key=value]", "(key:value)", "<key,value>"], "{key:value}"),
    ],
    "javascript": [
        ("What keyword declares a variable?", ["var", "int", "let", "Both var and let"], "Both var and let"),
        ("Which symbol is used for comments in JavaScript?", ["//", "#", "/*", "<!--"], "//"),
        ("Which company developed JavaScript?", ["Microsoft", "Google", "Netscape", "Oracle"], "Netscape"),
        ("What does NaN stand for?", ["Not a Name", "Not a Number", "No Any Name", "New Array Number"], "Not a Number"),
        ("What type is returned by typeof null?", ["object", "null", "undefined", "NaN"], "object"),
        ("How do you define a function?", ["function myFunc()", "def myFunc()", "fun myFunc()", "lambda myFunc()"], "function myFunc()"),
        ("Which operator compares both value and type?", ["==", "===", "!=", "="], "==="),
        ("What is 'undefined' in JS?", ["An error", "A function", "A type", "A keyword"], "A type"),
        ("What method converts JSON to object?", ["parseJSON()", "stringify()", "JSON.parse()", "JSON.toObject()"], "JSON.parse()"),
        ("Which method adds item to array?", ["push()", "add()", "insert()", "append()"], "push()"),
    ],
    "c++": [
        ("What is the output of: cout << 5 + 3 * 2;", ["16", "11", "10", "None"], "11"),
        ("Which keyword is used to define a class?", ["class", "struct", "object", "define"], "class"),
        ("What is the size of char in C++?", ["1 byte", "2 bytes", "4 bytes", "8 bytes"], "1 byte"),
        ("Which operator is used for pointer dereferencing?", ["*", "&", "%", "$"], "*"),
        ("What does 'new' do in C++?", ["Creates object", "Deletes object", "Allocates memory", "Both creates and allocates"], "Both creates and allocates"),
        ("Which header file is required for input/output?", ["iostream.h", "stdio.h", "stdlib.h", "conio.h"], "iostream.h"),
        ("What is the default access specifier for class members?", ["public", "private", "protected", "None"], "private"),
        ("Which function is used to find length of string?", ["length()", "size()", "strlen()", "strlength()"], "strlen()"),
        ("What does 'this' refer to in C++?", ["Current object", "Previous object", "Global variable", "None"], "Current object"),
        ("Which operator is used for scope resolution?", ["::", ".", "#", "&"], "::")
    ],

    "html": [
        ("What does HTML stand for?", ["Hyper Text Markup Language", "High Text Markup Language", "Hyperlink and Text Markup Language", "None"], "Hyper Text Markup Language"),
        ("Which tag is used for links?", ["<link>", "<a>", "<href>", "<url>"], "<a>"),
        ("What is the correct HTML for a line break?", ["<break>", "<br>", "<lb>", "<line>"], "<br>"),
        ("Which tag is used for the largest heading?", ["<h1>", "<h6>", "<heading>", "<head>"], "<h1>"),
        ("What does CSS stand for?", ["Cascading Style Sheets", "Colorful Style Sheets", "Creative Style Sheets", "Computer Style Sheets"], "Cascading Style Sheets"),
        ("Which attribute is used to define inline styles?", ["style", "font", "class", "styles"], "style"),
        ("What is the correct HTML for an image?", ["<img src='image.jpg'>", "<image src='image.jpg'>", "<img href='image.jpg'>", "<img link='image.jpg'>"], "<img src='image.jpg'>"),
        ("Which tag is used to create a list?", ["<list>", "<ul>", "<ol>", "<li>"], "<ul>"),
        ("What does <p> tag do?", ["Paragraph", "Picture", "Page", "Part"], "Paragraph"),
        ("Which tag is used for comments in HTML?", ["<!-- comment -->", "// comment", "# comment", "/ comment"], "<!-- comment -->")
    ],
    "dancing": [
        ("What is the basic step in ballet?", ["Plie", "Tendu", "Releve", "Saut"], "Plie"),
        ("Which dance style uses a barre?", ["Hip Hop", "Ballet", "Jazz", "Contemporary"], "Ballet"),
        ("What is a pirouette?", ["Spin on one leg", "Jump", "Slide", "Turn"], "Spin on one leg"),
        ("Which dance is known for its fast footwork?", ["Salsa", "Waltz", "Tango", "Breakdance"], "Breakdance"),
        ("What is the main focus of contemporary dance?", ["Technique", "Expression", "Speed", "Strength"], "Expression"),
        ("Which dance involves a partner?", ["Solo", "Group", "Duet", "None"], "Duet"),
        ("What is the term for a dance performance?", ["Recital", "Showcase", "Exhibition", "Performance"], "Recital"),
        ("What is a 'choreographer'?", ["Dance teacher", "Dance creator", "Dance performer", "Dance judge"], "Dance creator"),
        ("What is the term for a dance routine?", ["Choreography", "Sequence", "Routine", "Performance"], "Choreography"),
        ("What is the term for a dance competition?", ["Battle", "Contest", "Showdown", "Challenge"], "Battle")
    ],
    "painting": [
        ("What is the primary color?", ["Red", "Green", "Yellow", "Blue"], "Red"),
        ("What is the term for mixing colors?", ["Blending", "Merging", "Combining", "Mixing"], "Mixing"),
        ("Which medium uses water and pigment?", ["Oil", "Acrylic", "Watercolor", "Pastel"], "Watercolor"),
        ("What is a canvas?", ["Painting surface", "Brush type", "Color palette", "Easel"], "Painting surface"),
        ("What is the term for a painting of a person?", ["Portrait", "Landscape", "Still life", "Abstract"], "Portrait"),
        ("Which color is made by mixing blue and yellow?", ["Green", "Purple", "Orange", "Brown"], "Green"),
        ("What is the technique of applying paint with a brush?", ["Sculpting", "Drawing", "Brushing", "Painting"], "Painting"),
        ("What is the term for a painting of inanimate objects?", ["Portrait", "Landscape", "Still life", "Abstract"], "Still life"),
        ("What is the primary purpose of an easel?", ["Hold canvas", "Mix colors", "Store brushes", "Display art"], "Hold canvas"),
        ("What is the term for a painting style that emphasizes light and color?", ["Impressionism", "Realism", "Cubism", "Surrealism"], "Impressionism")
    ],
    "singing": [
        ("What is the vocal range of a soprano?", ["High", "Medium", "Low", "None"], "High"),
        ("What is a 'scale' in music?", ["Set of notes", "Type of song", "Vocal exercise", "Music genre"], "Set of notes"),
        ("What is the term for singing without accompaniment?", ["A cappella", "Solo", "Duet", "Chorus"], "A cappella"),
        ("What is vibrato?", ["Rapid pitch variation", "Sustained note", "Soft singing", "Loud singing"], "Rapid pitch variation"),
        ("What is a 'melody'?", ["Tune", "Rhythm", "Harmony", "Beat"], "Tune"),
        ("What is the term for a group of singers?", ["Choir", "Band", "Orchestra", "Ensemble"], "Choir"),
        ("What is the term for the high part in harmony?", ["Alto", "Tenor", "Bass", "Soprano"], "Soprano"),
        ("What is a 'lyric'?", ["Song words", "Music notes", "Vocal technique", "Singing style"], "Song words"),
        ("What is the term for a solo performance?", ["Recital", "Concert", "Soloist", "Performance"], "Recital"),
        ("What is the term for a song's main theme?", ["Verse", "Chorus", "Bridge", "Hook"], "Chorus")
    ],
    "react": [
        ("What is React?", ["JavaScript library", "Framework", "Language", "Tool"], "JavaScript library"),
        ("What is JSX?", ["JavaScript XML", "JavaScript Extension", "JavaScript Xtreme", "JavaScript Example"], "JavaScript XML"),
        ("What is a component in React?", ["Function", "Class", "Object", "All of the above"], "All of the above"),
        ("What is the purpose of 'props'?", ["State management", "Data passing", "Event handling", "None"], "Data passing"),
        ("What is 'state' in React?", ["Component data", "Global variable", "Function parameter", "None"], "Component data"),
        ("What is the purpose of 'useState'?", ["State management", "Event handling", "Data fetching", "None"], "State management"),
        ("What is 'useEffect' used for?", ["State management", "Side effects", "Event handling", "None"], "Side effects"),
        ("What is a 'key' in React?", ["Identifier", "State", "Prop", "Event"], "Identifier"),

        ("What is the purpose of 'render()'?", ["Display component", "Fetch data", "Handle events", "None"], "Display component"),
        ("What is 'ReactDOM'?", ["React library", "DOM manipulation", "State management", "None"], "DOM manipulation")
    ],
    "css": [
        ("What does CSS stand for?", ["Cascading Style Sheets", "Colorful Style Sheets", "Creative Style Sheets", "Computer Style Sheets"], "Cascading Style Sheets"),
        ("Which property is used to change the background color?", ["bgcolor", "background-color", "color", "background"], "background-color"),
        ("Which property is used to change the font size?", ["font-size", "text-size", "size", "font"], "font-size"),
        ("What is the correct CSS syntax?", ["{body:color:red;}", "body {color: red;}", "body:color=red;", "<body style='color:red;'>"], "body {color: red;}"),
        ("Which property is used to change the text color?", ["text-color", "color", "font-color", "text-style"], "color"),
        ("Which CSS property controls the text size?", ["text-size", "font-size", "text-style", "font-style"], "font-size"),
        ("Which property is used to set the spacing between lines?", ["line-height", "spacing", "text-spacing", "height"], "line-height"),
        ("Which property is used to set the width of an element?", ["width", "element-width", "size", "length"], "width"),
        ("Which property is used to set the height of an element?", ["height", "element-height", "size", "length"], "height"),
        ("Which property is used to set the margin of an element?", ["margin", "padding", "space", "border"], "margin")
    ],
    "photography": [
        ("What does ISO stand for?", ["International Standards Organization", "Image Stabilization Option", "Internal Sensor Output", "None"], "International Standards Organization"),
        ("What is aperture?", ["Opening in lens", "Shutter speed", "ISO setting", "None"], "Opening in lens"),
        ("What is shutter speed?", ["Time sensor exposed", "Aperture size", "ISO setting", "None"], "Time sensor exposed"),
        ("What is the rule of thirds?", ["Composition technique", "Lighting technique", "Camera setting", "None"], "Composition technique"),
        ("What is a DSLR?", ["Digital Single Lens Reflex", "Digital Sensor Lens Reflex", "Digital Single Lens Resolution", "None"], "Digital Single Lens Reflex"),
        ("What is a histogram?", ["Graph of tones", "Camera setting", "Lens type", "None"], "Graph of tones"),
        ("What is white balance?", ["Color temperature adjustment", "Exposure setting", "Aperture setting", "None"], "Color temperature adjustment"),
        ("What is depth of field?", ["Focus range", "Aperture size", "Shutter speed", "None"], "Focus range"),
        ("What is a prime lens?", ["Fixed focal length", "Zoom lens", "Wide-angle lens", "None"], "Fixed focal length"),
        ("What is a RAW file?", ["Unprocessed image", "Compressed image", "JPEG format", "None"], "Unprocessed image")
    ],
    "sketching": [
        ("What is the primary tool for sketching?", ["Pencil", "Pen", "Brush", "Charcoal"], "Pencil"),

        ("What is the term for light and shadow in drawing?", ["Contrast", "Shading", "Highlight", "None"], "Shading"),
        ("What is a sketch?", ["Quick drawing", "Detailed painting", "Sculpture", "None"], "Quick drawing"),
        ("What is the term for the outline of a drawing?", ["Contour", "Shape", "Form", "None"], "Contour"),
        ("What is the purpose of a sketch?", ["Planning", "Final artwork", "Coloring", "None"], "Planning"),
        ("What is the term for a rough drawing?", ["Draft", "Outline", "Sketch", "None"], "Sketch"),
        ("What is the term for a detailed drawing?", ["Illustration", "Rendering", "Sketch", "None"], "Illustration"),
        ("What is the term for a drawing of a person?", ["Portrait", "Landscape", "Still life", "None"], "Portrait"),
        ("What is the term for a drawing of objects?", ["Still life", "Portrait", "Landscape", "None"], "Still life"),
        ("What is the term for a drawing of a scene?", ["Landscape", "Portrait", "Still life", "None"], "Landscape")
    ],
    "acting": [
        ("What is the term for a performance in front of an audience?", ["Acting", "Performance", "Show", "None"], "Performance"),
        ("What is the term for a script?", ["Dialogue", "Screenplay", "Play", "None"], "Screenplay"),
        ("What is the term for a character's motivation?", ["Objective", "Goal", "Desire", "None"], "Objective"),
        (
        "What is the term for a rehearsal?", ["Practice", "Run-through", "Blocking", "None"], "Run-through"),
        ("What is the term for a stage direction?", ["Blocking", "Action", "Movement", "None"], "Blocking"),    
        ("What is the term for a monologue?", ["Solo speech", "Dialogue", "Scene", "None"], "Solo speech"),
        ("What is the term for a scene?", ["Act", "Sequence", "Moment", "None"], "Act"),
        ("What is the term for a character's backstory?", ["History", "Background", "Profile", "None"], "Background"),
        ("What is the term for a performance in front of a camera?", ["Filming", "Acting", "Shooting", "None"], "Filming"),
        ("What is the term for a character's emotional state?", ["Emotion", "Feeling", "State of mind", "None"], "State of mind")
    ],
        







    


    "java": [
    ("What is JVM?", ["Java Virtual Machine", "Java Very Modern", "Just Very Many", "Java Verification Model"], "Java Virtual Machine"),
    ("What is bytecode in Java?", ["Java source", "Machine code", "Intermediate code", "Garbage code"], "Intermediate code"),
    ("Which keyword is used to inherit a class?", ["implements", "inherits", "extends", "super"], "extends"),
    ("Which method is entry point in Java?", ["init()", "main()", "start()", "execute()"], "main()"),
    ("What is the size of int in Java?", ["2 bytes", "4 bytes", "8 bytes", "Depends on system"], "4 bytes"),
    ("Which collection is ordered?", ["Set", "List", "Map", "HashMap"], "List"),
    ("Which is not an access modifier?", ["public", "private", "protected", "internal"], "internal"),
    ("What is exception?", ["Runtime error", "Compiler bug", "Memory issue", "Design flaw"], "Runtime error"),
    ("Which loop is entry-controlled?", ["while", "do-while", "for", "Both while and for"], "Both while and for"),
    ("What does static mean?", ["Can’t be used", "Shared across instances", "Final", "Public"], "Shared across instances")
],
"sql": [
    ("Which keyword is used to get data?", ["FETCH", "GET", "SELECT", "RETRIEVE"], "SELECT"),
    ("What does WHERE do?", ["Adds row", "Filters rows", "Deletes row", "Orders results"], "Filters rows"),
    ("Which SQL clause is used to group rows?", ["SORT", "GROUP BY", "COLLATE", "MERGE"], "GROUP BY"),
    ("What is a primary key?", ["Unique identifier", "Foreign reference", "Optional ID", "Text value"], "Unique identifier"),
    ("Which SQL command modifies data?", ["SELECT", "UPDATE", "ALTER", "DESCRIBE"], "UPDATE"),
    ("What type of JOIN returns all rows?", ["LEFT", "FULL OUTER", "INNER", "RIGHT"], "FULL OUTER"),
    ("What is SQL injection?", ["Security flaw", "Query type", "Join strategy", "Database syntax"], "Security flaw"),
    ("How do you remove a table?", ["DROP", "DELETE", "REMOVE", "CLEAR"], "DROP"),
    ("What does COUNT(*) do?", ["Sum values", "Find max", "Count rows", "None"], "Count rows"),
    ("Which symbol is used for wildcard?", ["#", "*", "%", "&"], "%")
]


    
}

with app.app_context():
    # ✅ Prevent duplicate insertion
    existing_tests = SkillTest.query.first()
    if existing_tests:
        print("⚠️ Skill tests already exist. Skipping insertion.")
    else:
        for skill, questions in tests_data.items():
            for q_text, options, answer in questions:
                test = SkillTest(
                    skill_name=skill,
                    question=q_text,
                    options=options,
                    correct_answer=answer
                )
                db.session.add(test)
        db.session.commit()
        print("✅ All skill test questions inserted.")
