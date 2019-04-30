class Opt(object):
    def __init__(self, args):
        self.spec       = args.spec_view
        self.series     = args.series_view
        self.waterfall  = args.waterfall_plot
        self.contour    = args.contour_plot

        self.scalogram  = args.scalogram_plot
        self.SaveFig    = not args.show_gui
        self.show_gui   = args.show_gui
        self.raw_data   = args.raw_data
        self._3ax_raw_data   = args._3ax_raw_data
        self.fea_data   = args.fea_data
        
        self.DataPath = args.data
        splitted_path = self.DataPath.rsplit('/',1) 
        self.DataDir = splitted_path[0]+'/'
        self.filename = splitted_path[1]
        
        if args.axis == None:
            self.axis = None
        else:
            self.axis = args.axis.rsplit('=',1)[0]
        
        if args.record_range == None:
            self.record_range = None
        else:
            self.record_range = args.record_range.rsplit('=',1)[0].rsplit(',',1)
            self.record_range = list(map(int, self.record_range))

