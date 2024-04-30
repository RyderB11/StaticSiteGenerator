from textnode import TextNode
def main():
    # These are your dummy values
    text = "This is a text node"
    text_type = "bold"  # It looks like you named the variable 'bold', but 'text_type' might be more descriptive
    url = "https://boot.dev"
    # here is a fake node to text with our dummy values to make sure its working.
    node = TextNode(text, text_type, url)

    print(node)
# not sure wht main is named like this, will look it up
if __name__ == "__main__":
    main()
