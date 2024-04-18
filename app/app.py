#imports
import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

#use built-in function to load the Palmser Penguins dataset
df = palmerpenguins.load_penguins()

#Title the dashboard
ui.page_opts(title="Laura's Penguins Dashboard", fillable=True)

#create sidebar for user interaction
with ui.sidebar(title="Filter Controls", style="background-color:ghostwhite"):
    #create a slider input to filter for body_mass_g
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    #create checkboxes to filter by penguin species
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    #add horizontal rule to sidebar
    ui.hr()
    #add hyperlinks
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/lauravos/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/lauravos/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

#(main section with value boxes and cards for scatterplot and dataframe)

#add value boxes
with ui.layout_column_wrap(fill=False):
    #add value box for number of penguins
    with ui.value_box(showcase=icon_svg("earlybirds"), theme="bg-gradient-blue-purple"):
        "Number of Penguins"

        @render.text
        def count():
            return filtered_df().shape[0]
            
    #add value box for average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal"), theme="bg-gradient-blue-purple"):
        "Average Bill Length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"
            
    #add value box for average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical"), theme="bg-gradient-blue-purple"):
        "Average Bill Depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

#add scatterplot and dataframe
with ui.layout_columns():
    #scatterplot
    with ui.card(full_screen=True, style="background-color:ghostwhite"):
        ui.card_header("Bill Length and Depth", style="background-color:cornflowerblue")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )
    #dataframe
    with ui.card(full_screen=True, style="background-color:ghostwhite"):
        ui.card_header("Penguin Data", style="background-color:cornflowerblue")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm" ,
                "bill_depth_mm" ,
                "body_mass_g",
            ]

            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")

#define a reactive calc to make the filters function
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
