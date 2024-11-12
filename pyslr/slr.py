import json

import pandas as pd
from pybtex.database.input import bibtex
from matplotlib.ticker import MaxNLocator

from radar_chart import *

with open('config.json', 'r') as file:
    config = json.load(file)

root_dir = config["root_dir"]

slr_articles_path = os.path.join(root_dir, config["articles_file_name"])
slr_authors_path = os.path.join(root_dir, config["authors_file_name"])
references_path = os.path.join(root_dir, config["references_folder"])
bib_path = os.path.join(root_dir, config["references_file_name"])

dimensions = config["dimensions"]
table_dimensions = config["table_dimensions"]
stacked_dimensions = config["stacked_dimensions"]
geography_levels = config["geography_levels"]
radar_dimensions = config["radar_dimensions"]
bib_names = config["database_names"]

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.sans-serif'] = ['Century']
plt.rcParams['font.size'] = 8

df_articles = pd.DataFrame()
df_authors = pd.DataFrame()

num_studies = 0


# Graph functions
def plot_line(dimension, dim_count_dict):
    fig, ax = plt.subplots()
    labels = [value.replace(" ", "\n") for value in list(dim_count_dict.keys())]
    bars = ax.plot(labels, dim_count_dict.values())
    ax.set_title(f"{dimension} frequency chart (n = {num_studies} studies)")
    if len(dim_count_dict) > 6:
        plt.xticks(rotation=35)
    ax.set_xlabel(f"{dimension}")
    ax.set_ylabel("Frequency")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis='y')
    plt.savefig(os.path.join(root_dir, f"figures\\{dimension}_freq.pdf"), format="pdf", bbox_inches="tight")


def plot_freq(dimension, dim_count_dict):
    fig, ax = plt.subplots()
    labels = [value.replace(" ", "\n") for value in list(dim_count_dict.keys())]
    bars = ax.bar(labels, dim_count_dict.values())
    ax.bar_label(bars)
    ax.set_title(f"{dimension} frequency chart (n = {num_studies} studies)")
    if len(dim_count_dict) > 6:
        plt.xticks(rotation=35)
    if len(dim_count_dict) <= 3:
        ax.set_aspect(0.3)
    ax.set_xlabel(f"{dimension}")
    ax.set_ylabel("Frequency")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis='y')
    plt.savefig(os.path.join(root_dir, f"figures\\{dimension}_freq.pdf"), format="pdf", bbox_inches="tight")


def plot_freq_stacked(dimension, stacked_dimension, dim_count_dict):
    fig, ax = plt.subplots()
    x = list(dim_count_dict.keys())
    y_labels = list(dim_count_dict[x[0]].keys())
    y_list = [[] for _ in y_labels]
    ax.set_title(f"{dimension} and {stacked_dimension} frequency chart (n = {num_studies} studies)")

    for i, label in enumerate(y_labels):
        for key, item in dim_count_dict.items():
            y_list[i].append(item[label])

    y_list = [np.array(x) for x in y_list]

    bottom = np.zeros(len(x))
    bars = None
    for y in y_list:
        bars = ax.bar(x, y, bottom=bottom)
        labels = [f"{int(bar.get_height())}" if bar.get_height() > 0.2 else '' for bar in bars]
        ax.bar_label(bars, labels=labels, label_type='center', color='white')
        bottom += y
    ax.bar_label(bars)

    ax.legend(y_labels)
    ax.set_xlabel(f"{dimension}")
    ax.set_ylabel("Frequency")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis='y')
    plt.savefig(os.path.join(root_dir, f"figures\\{dimension}_{stacked_dimension}_freq.pdf"), format="pdf",
                bbox_inches="tight")


def plot_freq_h(dimension, dim_count_dict):
    fig, ax = plt.subplots()
    bars = ax.barh(list(dim_count_dict.keys()), dim_count_dict.values())
    ax.bar_label(bars)
    ax.set_title(f"{dimension} frequency chart (n = {num_studies} studies)")
    ax.set_ylabel(f"{dimension}")
    ax.set_xlabel("Frequency")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis='x')
    plt.savefig(os.path.join(root_dir, f"figures\\{dimension}_freq.pdf"), format="pdf", bbox_inches="tight")


def plot_pie(dimension, data_dict):
    fig, ax = plt.subplots()
    ax.pie(data_dict.values(), labels=[f"{label} ({data_dict[label]})" for label in data_dict.keys()],
           autopct='%1.0f%%')
    ax.set_title(f"{dimension} frequency chart (n = {num_studies} studies)")
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()

    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)
    plt.savefig(os.path.join(root_dir, f"figures\\{dimension}_freq.pdf"), format="pdf", bbox_inches="tight")


def plot_graph(dimension, data_dict, graph_type):
    if graph_type == "B":
        plot_freq(dimension, data_dict)
    elif graph_type == "BH":
        plot_freq_h(dimension, data_dict)
    elif graph_type == "P":
        plot_pie(dimension, data_dict)
    elif graph_type == "L":
        plot_line(dimension, data_dict)


def create_dimension_plots():
    for dimension in dimensions.keys():
        try:
            dim_col = df_articles[dimension]
        except:
            print(f"Dimension '{dimension}' is missing. Skipping.")
            continue
        dim_count_dict = {}
        for dims in dim_col:
            dims_split = str(dims).split(",")
            for d in dims_split:
                dim = d.strip()
                if '\"' in dim:
                    dim = dim.replace("\"", "")
                if dim in dim_count_dict:
                    dim_count_dict[dim] += 1
                else:
                    dim_count_dict[dim] = 1

        if dimension == "Year":
            dim_count_dict = dict(sorted(dim_count_dict.items()))
        else:
            dim_count_dict = dict(sorted(dim_count_dict.items(), key=lambda x: x[1], reverse=True))

        for graph_type in dimensions[dimension]:
            if graph_type == "BH":
                dim_count_dict = dict(sorted(dim_count_dict.items(), key=lambda x: x[1]))
            plot_graph(dimension, dim_count_dict, graph_type)

    plt.show()


def create_stacked_dimension_plots():
    for dim1, dim2 in stacked_dimensions:
        stacked_dim_dict = {}
        stacked_dim_values = set()
        for index, row in df_articles.iterrows():
            stacked_dim_values.add((str(row[dim2]), 0))

        for index, row in df_articles.iterrows():
            x = str(row[dim1])
            if x not in stacked_dim_dict:
                stacked_dim_dict[x] = dict(stacked_dim_values)

            y = row[dim2]

            stacked_dim_dict[x][y] += 1

        if dim1 == "Year":
            stacked_dim_dict = dict(sorted(stacked_dim_dict.items()))

        print(stacked_dim_dict)
        plot_freq_stacked(dim1, dim2, stacked_dim_dict)

    plt.show()


def create_radar_plots():
    half = int(len(df_articles.index) / 2)
    df1 = df_articles.iloc[0:half]
    df2 = df_articles.iloc[half::]

    plot_radar_many(df1, radar_dimensions, root_dir, "dimensions_radar_1")
    plot_radar_many(df2, radar_dimensions, root_dir, "dimensions_radar_2")


def create_geography_plots():
    for geography in geography_levels.keys():
        combination_list = []
        geography_count = {}
        for index, row in df_authors.iterrows():
            study = row["Study"]
            value = row[geography]
            key = f"{study}_{value}"
            if value not in geography_count:
                geography_count[value] = 0
            if key not in combination_list:
                combination_list.append(key)
                geography_count[value] += 1
        geography_count = dict(sorted(geography_count.items(), key=lambda x: x[1]))
        for graph_type in geography_levels[geography]:
            plot_graph(geography, geography_count, graph_type)
    plt.show()


def get_venue(bibtex_type):
    if bibtex_type == "inproceedings":
        return "Conference"
    if bibtex_type == "article":
        return "Journal"
    if bibtex_type == "incollection" or bibtex_type == "inbook":
        return "Book Chapter"
    if bibtex_type == "book":
        return "Book"


def get_publication(entry):
    publication = False
    if entry.type == "inproceedings" or entry.type == "conference":
        publication = entry.fields.get("booktitle", False)
    elif entry.type == "article":
        publication = entry.fields.get("journal", False)
    elif entry.type == "incollection" or entry.type == "inbook":
        publication = entry.fields.get("booktitle", False)
    elif entry.type == "book":
        publication = entry.fields.get("booktitle", False)

    if not publication:
        publication = entry.fields.get("journal")

    return publication


def get_main_author(entry):
    authors = entry.persons["author"]
    return " ".join(authors[0].last_names)


def get_authors_list(entry):
    authors = entry.persons["author"]
    return "#".join([a.__str__() for a in authors])


def get_word_acronym(word):
    if word == "N/A" or word == '"N/A"':
        return "-"
    elif len(word) <= 2 or word.isupper():
        return word.upper()
    else:
        return word.upper()[0]


def get_dimension_value_acronym(dimension_value, existing_acronyms):
    if dimension_value in existing_acronyms.keys():
        return existing_acronyms[dimension_value]
    
    words = dimension_value.replace("-", " ").split()
    acronym = ""
    if len(words) > 1:
        for word in words:
            acronym += get_word_acronym(word)
    else:
        acronym = get_word_acronym(words[0])

    if acronym in existing_acronyms.values():
        acronym += dimension_value[1].lower()
    return acronym


# Given a Bibtex file (at "bib_path"), update the "articles" and "authors" files
def update_slr_tables_from_bibtex():
    parser = bibtex.Parser()
    bibtex_data = parser.parse_file(bib_path)
    new_entries = []
    for entry in bibtex_data.entries.values():
        title = entry.fields['title']
        if len(df_articles.loc[df_articles['Title'] == title].index) == 0:
            new_entries.append(entry)

    print(f"Number of new entries: {len(new_entries)}")
    df_articles_new = df_articles.copy()
    df_authors_new = df_authors.copy()
    for new_entry in new_entries:
        study_number = len(df_articles_new.index) + 1
        if study_number < 10:
            study_number = f"S0{study_number}"
        else:
            study_number = f"S{study_number}"

        new_article_row = {"Study": study_number,
                           "Citation": new_entry.key,
                           "Year": int(new_entry.fields['year']),
                           "Venue": get_venue(new_entry.type),
                           "Title": new_entry.fields['title'],
                           "Comments": "Put your comments about this article here...",
                           "Publication": get_publication(new_entry),
                           "Author": get_main_author(new_entry) + " et al.",
                           "Authors": get_authors_list(new_entry),
                           "DOI": new_entry.fields['doi'],
                           "Total": 0,
                           }
        df_articles_new = df_articles_new.append(new_article_row, ignore_index=True)
        # print(new_article_row)
        for author in list(new_entry.persons["author"]):
            new_author_row = {"Study": study_number,
                              "Citation": new_entry.key,
                              "Year": int(new_entry.fields['year']),
                              "Venue": get_venue(new_entry.type),
                              "Title": new_entry.fields['title'],
                              "Publication": get_publication(new_entry),
                              "Author": author.__str__(),
                              "Department": "Blank", "Institution": "Blank", "City": "Blank", "Country": "Blank",
                              "Continent": "Blank",
                              }
            df_authors_new = df_authors_new.append(new_author_row, ignore_index=True)
    df_articles_new.to_excel(config["articles_file_name"], index=False)
    df_authors_new.to_excel(config["authors_file_name"], index=False)


# Given two Bibtex files from the same database, return a .bib file with the new articles (removing duplicates)
def get_new_entries():
    for bib in bib_names:
        parser = bibtex.Parser()
        bib_prev_data = parser.parse_file(os.path.join(references_path, f"{bib}_old.bib"))
        parser = bibtex.Parser()
        bib_new_data = parser.parse_file(os.path.join(references_path, f"{bib}.bib"))

        duplicates = []
        for old_entry in bib_prev_data.entries.values():
            old_title = old_entry.fields['title']
            for new_entry in bib_new_data.entries.values():
                new_title = new_entry.fields['title']
                if old_title == new_title:
                    duplicates.append(new_entry)

        for d in duplicates:
            bib_new_data.entries.pop(d.key)

        print(len(duplicates))
        print(len(bib_new_data.entries))

        bib_new_data.to_file(os.path.join(references_path, f"{bib}_new_entries.bib"))


def create_table_files_from_bibtex():
    df_articles_new = pd.DataFrame()
    df_authors_new = pd.DataFrame()
    parser = bibtex.Parser()
    bibtex_data = parser.parse_file(bib_path)
    articles_list = []
    authors_list = []
    for new_entry in bibtex_data.entries.values():
        study_number = len(df_articles_new.index) + 1
        if study_number < 10:
            study_number = f"S0{study_number}"
        else:
            study_number = f"S{study_number}"

        new_article_row = {"Study": study_number,
                           "Citation": new_entry.key,
                           "Year": int(new_entry.fields['year']),
                           "Venue": get_venue(new_entry.type),
                           "Title": new_entry.fields['title'],
                           "Comments": "Put your comments about this article here...",
                           "Publication": get_publication(new_entry),
                           "Author": get_main_author(new_entry) + " et al.",
                           "Authors": get_authors_list(new_entry),
                           "DOI": new_entry.fields['doi'],
                           "Total": 0,
                           }
        articles_list.append(new_article_row)
        # df_articles_new = df_articles_new.append(new_article_row, ignore_index=True)
        for author in list(new_entry.persons["author"]):
            new_author_row = {"Study": study_number,
                              "Citation": new_entry.key,
                              "Year": int(new_entry.fields['year']),
                              "Venue": get_venue(new_entry.type),
                              "Title": new_entry.fields['title'],
                              "Publication": get_publication(new_entry),
                              "Author": author.__str__(),
                              "Department": "Blank", "Institution": "Blank", "City": "Blank", "Country": "Blank",
                              "Continent": "Blank",
                              }
            authors_list.append(new_author_row)
            # df_authors_new = df_authors_new.append(new_author_row, ignore_index=True)
    df_articles_new = pd.DataFrame(articles_list)
    df_authors_new = pd.DataFrame(authors_list)
    df_articles_new.to_excel(slr_articles_path, index=False)
    df_authors_new.to_excel(slr_authors_path, index=False)
    return df_articles_new, df_authors_new


def create_latex_information_table():
    with open('info.tex', 'w') as f:
        f.write("\\begin{tabular}{lllll}\n")
        f.write("\\toprule\n")
        f.write("Study & Year & Citation & Title & Publication \\\\[0.1cm]\n")
        f.write("\\midrule\n")

        for index, row in df_articles.iterrows():
            clean_title = str(row['Title']).replace('&', '\\&').replace('%', '\\%')
            clean_pub = str(row['Publication']).replace('&', '\\&').replace('%', '\\%')
            f.write(f"{row['Study']} & {row['Year']} & \\cite" + "{" + row['Citation'] + "}" + f" & {clean_title} "
                                                                                               f"& {clean_pub} \\\\[0.2cm]\n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.close()


def create_latex_summary_table():
    dim_acronyms = {k: {} for (k, _) in table_dimensions.items()}
    with open('summary.tex', 'w') as f:
        f.write("\\begin{tabular}{" + "l" * (len(table_dimensions) + 1) + "}\n")
        f.write("\\toprule\n")

        column_line = "Study & " + " & ".join(table_dimensions.keys()) + "\\\\[0.1cm]\n"
        f.write(column_line)
        f.write("\\midrule\n")

        for index, row in df_articles.iterrows():
            line_list = ["\\cite{" + row['Citation'] + "}"]
            for dimension in table_dimensions.keys():
                dim_values = row[dimension].split(',')
                acronym_values = []
                for v in dim_values:
                    value = v.strip()
                    acronym = get_dimension_value_acronym(value, dim_acronyms[dimension])
                    if value not in dim_acronyms[dimension].keys():
                        print(value)
                        dim_acronyms[dimension][value] = acronym
                    acronym_values.append(acronym)
                acronym_values.sort()
                line_list.append(", ".join(acronym_values))
            line = " & ".join(line_list) + " \\\\[0.2cm]\n"
            f.write(line)
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.close()
    print(dim_acronyms)


def init():
    global df_articles
    global df_authors
    global num_studies

    try:
        df_articles = pd.read_excel(slr_articles_path)
        num_studies = len(df_articles.index)
        df_authors = pd.read_excel(slr_authors_path)
    except:
        choice = input("The tables could not be read. Do you wish to load from a Bibtex file? Y/N")
        if choice == "Y":
            df_articles, df_authors = create_table_files_from_bibtex()
            num_studies = len(df_articles.index)
        print("Tables created. You can now fill the tables with manual information")


def display_menu():
    print("--- Plots")
    print("1. Create dimension plots")
    print("2. Create bibliometric plots")
    print("3. Create radar plots")
    print("4. Create stacked dimension plots")
    print("--- LaTeX utilities")
    print("5. Update Table from Bibtex")
    print("6. Get reference difference")
    print("7. Create LaTeX information table")
    print("8. Create LaTeX summary table")
    print("(9. Exit)\n")


def main():
    print("PySLR\n")
    while True:
        init()
        display_menu()
        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            create_dimension_plots()
        elif choice == '2':
            create_geography_plots()
        elif choice == '3':
            create_radar_plots()
        elif choice == '4':
            create_stacked_dimension_plots()
        elif choice == '5':
            update_slr_tables_from_bibtex()
        elif choice == '6':
            get_new_entries()
        elif choice == '7':
            create_latex_information_table()
        elif choice == "8":
            create_latex_summary_table()
        elif choice == '9':
            print("Exiting. See you soon!")
            break
        else:
            print("Invalid choice. Please try again.")
        print("\n")


if __name__ == "__main__":
    main()
