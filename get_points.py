class Point:
    def __init__(self,node_name: str = "M1502_P",block_name: str,px: float,py: float,layer: str = 'TR_PNT',symbol: str = '1502',mark: str = ''):
        self.node_name = node_name
        self.block_name = block_name
        self.px = px
        self.py = py
        self.layer = layer
        self.symbol = symbol
        self.mark = mark
    