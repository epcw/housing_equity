import dash
import dash_core_components as dcc
import dash_html_components as html

def Template() :
    template = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <meta name="description" content="The Center for Equitable Policy in a Changing World (EPCW), a non&#x2d;partisan group researching the effects of changes in society &#038; the environment on policy."/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <meta property="og:image" content="https://equitableworld.org/wp-content/uploads/2020/07/wordmark-og.png"/>
    <meta property="og:locale" content="en_US"/>
    <meta property="og:type" content="website"/>
    <meta property="og:title" content="Center for Equitable Policy in a Changing World | Pro pluribus"/>
    <meta property="og:description" content="The Center for Equitable Policy in a Changing World (EPCW), a non&#x2d;partisan group researching the effects of changes in society &#038; the environment on policy."/>
    <meta property="og:url" content="https://equitableworld.org/"/>
    <meta property="og:site_name" content="Center for Equitable Policy in a Changing World"/>
    <meta name="twitter:card" content="summary_large_image"/>
    <meta name="twitter:title" content="Center for Equitable Policy in a Changing World | Pro pluribus"/>
    <meta name="twitter:description" content="The Center for Equitable Policy in a Changing World (EPCW), a non&#x2d;partisan group researching the effects of changes in society &#038; the environment on policy."/>
    <meta name="twitter:image" content="https://equitableworld.org/wp-content/uploads/2020/07/wordmark-og.png"/>
            <link rel='stylesheet' id='chld_thm_cfg_ext1-css' href='https://fonts.googleapis.com/css?family=Barlow&#038;ver=5.4' type='text/css' media='all'/>
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            <div id="header" class="c-layout-header c-layout-header-3 c-layout-header-3-custom-menu c-layout-header-dark-mobile"><div class="c-navbar">
                <div class="container-fluid">
                    <div class="c-navbar-wrapper clearfix">
                        <div class="c-brand c-pull-left">
                            <a href="https://equitableworld.org/" class="c-logo"><img src="https://equitableworld.org/wp-content/uploads/2020/06/wordmark-logowide.png" alt="Logo" class="c-desktop-logo" width="300">
                            </a>  <div id="mobile-menu">
    <a href="/">Dashboards Home</a>
    <a href="https://equitableworld.org">Center Homepage</a>
    <a href="https://equitableworld.org/research">Research</a>
    <a href="https://equitableworld.org/events">Events</a>
    <a href="https://equitableworld.org/podcast">Podcast</a>
    <a href="https://equitableworld.org/About">About</a>
  </div>
  <a href="javascript:void(0);" class="icon" onclick="mobilecollapse()">
    <i class="fa fa-bars"></i>
  </a>
                                            </div>
                        <nav class="c-mega-menu c-pull-right c-mega-menu-dark c-mega-menu-dark-mobile c-fonts-uppercase c-fonts-bold">
                            <ul id="menu-main" class="nav navbar-nav c-theme-nav"><li id="nav-menu-item-24" class=" menu-item menu-item-type-post_type menu-item-object-page menu-item-home current-menu-item page_item page-item-2 current_page_item c-active"><a href="https://equitableworld.org/" class="c-link">Home</a></li>
        <li id="nav-menu-item-93" class=" menu-item menu-item-type-post_type menu-item-object-page"><a href="https://equitableworld.org/research/" class="c-link">Research</a>
<ul class="dropdown-menu c-menu-type-classic c-pull-left">
                <li id="nav-menu-item-607" class=" menu-item menu-item-type-custom menu-item-object-custom"><a href="/koppen">Measuring Climate Change</a></li>
                <li id="nav-menu-item-610" class=" menu-item menu-item-type-custom menu-item-object-custom"><a href="http://dashboards.equitableworld.org/">Dashboards &#038; Interactives</a></li>
                </ul>
</li>
        <li id="nav-menu-item-158" class=" menu-item menu-item-type-post_type menu-item-object-page"><a href="https://equitableworld.org/events/" class="c-link">Events</a></li>
        <li id="nav-menu-item-171" class=" menu-item menu-item-type-post_type_archive menu-item-object-podcast"><a href="https://equitableworld.org/podcast/" class="c-link">Podcast</a></li>
        <li id="nav-menu-item-21" class=" menu-item menu-item-type-post_type menu-item-object-page"><a href="https://equitableworld.org/about/" class="c-link">About us</a></li>
        </ul>
                        </nav>
                    </div>
                </div>
            </div></div>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
            <div></div>
        </body>
    </html>
    '''
    return template
