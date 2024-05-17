class HTMLNode:
    def __init__(self,
                    tag: str =None,
                    value: str =None,
                    children: list =None,
                    props: dict =None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        if self.children:
            children_html = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    def props_to_html(self):
        result = ""
        if self.props is None: # according to boots, "Using `is None` for comparison to `None` is a bit more pythonic", i was using "== None"
            return result      # here the instructions said return and empty string so i had "", but i guess thats redundant if i have a variable thats an empty string
        else:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
        return result
    
    def add_child(self, child):
        self.children.append(child)

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props)  #the super() init inputs need to match that of the parent, not the child. or it will swap things out of order. i had value and tag swapped to match the child. so the code results were swapping. 

    def to_html(self):
        if self.tag is None:
            return self.value
        elif self.value is None or self.value == "":
            raise ValueError
        else:
            # this code was a huge pain, i could have just did this all in one line like below, but i kept trying to make and empty string and append things as they came. dont forget stuff like the parent functions. this example code uses the prop_to_html function. 
            # Making this code 10X easier and easier to work with. I dont even wanna remmeber what i was trying. 
            props_html = self.props_to_html()
            if props_html:  # Check if props_html is not empty before appending
                return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"   
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None or self.tag == '':
            raise ValueError
        elif self.children is None or len(self.children) == 0:
            raise ValueError('No Children supplied')
        else:
            return f"<{self.tag}>{self.render_children_html()}</{self.tag}>"
        
    def render_children_html(self):
        children_html = ''
        for child in self.children:
            children_html += child.to_html()
        return children_html
    
