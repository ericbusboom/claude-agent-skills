# TODO

I've created a To Do directory, and I'd like to add this to the process. The To Do directory is going to be for the software engineer to be able to add ideas that we have a place to put them while you're off doing something else, right? I often can't put those into the chat because the chat's busy or we're talking about something else. I don't want to confuse you. So I can go create a separate file, a separate entry in the To Do's.

The To Do directory is very unstructured if you look in the To Do's they might
cover multiple things so you need to look at the files and there are not
sprints, they're not tickets, they're ideas, and what you probably will be doing
is going through and mining that for future sprints. So that's something that we
should do.

This is a lightly structured script. The to-do list is lightly structured, and so I think we've got some maintenance processes for it. One of them you can implement in your Claude program is you implement something that cleans up the to-do directory. What it does is it takes the files and looks for level one headings and it breaks the to-dos up by level one headings. So if you have a to-do file in there when you run the Claude clean up to-dos script, it's going to a file and says "Oh, there's three level one headings in this file" and then it extracts each of those level one sections and creates a new file for it and then deletes the original file.

Okay, then we're going to treat to-dos like tickets. That is, when you decide to put one into a sprint, you're going to talk to the user about it, make sure you understand it. Move that text into the sprint for part of what the sprint's going to do. And then move the to-do file to done. Right, so it will be to-do/done.