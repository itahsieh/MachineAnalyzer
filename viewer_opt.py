PlotKey = ['series','spec','waterfall','contour','scalogram','velocity']


class Opt(object):
    def __init__(self, args):
        # ouput device
        self.SaveFig    = not args.show_gui
        self.show_gui   = args.show_gui
        # data type tag
        self.raw_data   = args.raw_data
        self._3ax_raw_data   = args._3ax_raw_data
        self.fea_data   = args.fea_data
        # input path
        self.DataPath = args.data
        splitted_path = self.DataPath.rsplit('/',1) 
        self.DataDir  = splitted_path[0]+'/'
        self.filename = splitted_path[1]
        # sampling rate
        self.sampling = float(args.sampling)
        
        self.bias = float(args.bias)
        self.IV = float(args.IV)
        self.threshold = float(args.threshold)
        
        if args.axis == None:
            self.axis = None
        else:
            self.axis = args.axis.rsplit('=',1)[0]
        
        if args.record_range == None:
            self.record_range = None
        else:
            self.record_range = args.record_range.rsplit('=',1)[0].rsplit(',',1)
            self.record_range = list(map(int, self.record_range))
        
        self.PlotType = args.plot.rsplit('=',1)[1].rsplit(',')
        
        
        for key in self.PlotType:
            if key not in PlotKey:
                print('plot keyword is not matched:',key)
                exit(2)
