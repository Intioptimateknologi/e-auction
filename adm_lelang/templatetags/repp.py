from django import template

register = template.Library()

def repl(text):
    return text.replace('/','_')

register.filter('repl', repl)