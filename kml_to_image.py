import cairo
import mapnik

KML_PATH = "./data/kml/cb_2020_us_county_20m.kml"

WIDTH = 1500
HEIGHT = 1500
# Used for layer
# Default proj4 code "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
PROJ_CODE = "init=espg:4326"
# OpenStreetMap projection
PROJECTION = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs"
STYLE_NAME = "My Style"

m = mapnik.Map(width=WIDTH, height=HEIGHT, srs=PROJECTION)
m.background = mapnik.Color(0, 0, 0, 0)

bbox = mapnik.Box2d(-10000000, 2000000, -4000000, -19000000)
m.zoom_to_box(bbox)

s = mapnik.Style()
r = mapnik.Rule()

polygon_symbolizer = mapnik.PolygonSymbolizer()
polygon_symbolizer.fill_opacity = 0.0
r.symbolizers.append(polygon_symbolizer)

line_symbolizer = mapnik.LineSymbolizer()
line_symbolizer.stroke = mapnik.Color("black")
line_symbolizer.stroke_width = 0.1
r.symbolizers.append(line_symbolizer)

s.rules.append(r)
m.append_style(STYLE_NAME, s)

# Layer config
# # lyr = mapnik.Layer("path", PROJ_CODE)
lyr = mapnik.Layer("path", PROJECTION)
# layer=name of layer to use within datasource
lyr.datasource = mapnik.Ogr(file=KML_PATH, layer="cb_2020_us_county_20m")
lyr.styles.append(STYLE_NAME)
m.layers.append(lyr)
mapnik.render_to_file(m, "test.png", "png")
# mapnik.render_to_file(m,'./path.png', 'png')

# file = open("./path.pdf", "wb")
# surface = cairo.PDFSurface(file.name, m.width, m.height)
# mapnik.render(m, surface)
# surface.finish()
