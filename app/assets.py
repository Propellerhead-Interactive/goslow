from flask_assets import Bundle

common_css = Bundle('css/bootstrap.css', 'css/tether.min.css', 'css/pikaday.css')

common_js = Bundle('js/tether.min.js','js/bootstrap.min.js', 'js/moment.min.js', 'js/pikaday.js', 'js/jquery.mask.min.js')
