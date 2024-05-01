class HTMLNode:
    def __init__(self, tag: str =None, value: str =None, children: list =None, props: dict =None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        if self.props is None: # according to boots, "Using `is None` for comparison to `None` is a bit more pythonic", i was using "== None"
            return result      # here the instructions said return and empty string so i had "", but i guess thats redundant if i have a variable thats an empty string
        else:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
        return result
