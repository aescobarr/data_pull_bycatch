from downloader import auth, get_project_observations
import settings
import json
import datetime
import csv


def write_heatmap_data(data):
    print("Writing heat map data to file...")
    with open(settings.home_dir + 'heat_data.js', 'w') as outfile:
        out_array = []
        for d in data:
            if not d[settings.latitude_field_name] is None and not d[settings.longitude_field_name] is None:
                try:
                    out_array.append("[{0},{1}]".format(d[settings.latitude_field_name],d[settings.longitude_field_name]))
                except KeyError:
                    pass
        outfile.write("var heat_data = [{0}];".format(",".join(out_array)))
    print("Done writing heat map data to file.")


def write_csv_time_histo_year(data):
    print("Writing year time histo to file...")
    now = datetime.datetime.now()
    current_year = now.year
    time_data = []
    time_data_map = {}
    for i in range(2019, current_year+1):
        time_data.append( [str(i), 0] )
        time_data_map[i] = time_data[-1]
    for d in data:
        for tag in d['tag_list']:
            try:
                possible_date = datetime.datetime.strptime(tag, '%d/%m/%Y')
                date_year = possible_date.year
                time_data_map[date_year][1] = time_data_map[date_year][1] + 1
            except ValueError:
                #Not a date
                pass
            except KeyError:
                #Year not in array
                pass
    # and then, write the csv
    with open(settings.home_dir + 'histo_year_data.csv', 'w') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in time_data:
            f_writer.writerow(line)


def write_csv_time_histo_15(data):
    print("Writing 15 day time histo to file...")
    now = datetime.datetime.now()
    current_year = now.year
    time_data = []
    for month in range(1,13):
        time_data.append(['1-14/' + str(month) + '/' + str(current_year), 0])
        time_data.append(['15+/' + str(month) + '/' + str(current_year), 0])
    for d in data:
        for tag in d['tag_list']:
            try:
                possible_date = datetime.datetime.strptime(tag, '%d/%m/%Y')
                if possible_date.year == current_year:
                    date_month = possible_date.month
                    date_day = possible_date.day
                    month_index = (date_month - 1) * 2
                    day_index = 0 if date_day < 15 else 1
                    time_data[month_index + day_index][1] = time_data[month_index + day_index][1] + 1
            except ValueError:
                #Not a date
                pass
    # and then, write the csv
    with open(settings.home_dir + 'histo_15_data.csv', 'w') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in time_data:
            f_writer.writerow(line)


def write_csv_class_histo(data):
    print("Writing class data to file...")
    with open(settings.home_dir + 'taxo.json') as f:
        taxo_data = json.load(f)
    upper_taxo_map = {}
    csv_data = {}
    for group in taxo_data:
        try:
            # it has children, is an upper group
            for child in group['children']:
                upper_taxo_map[child['val']] = group['loc_name']
        except KeyError:
            pass
        finally:
            upper_taxo_map[group['val']] = group['loc_name']
    for d in data:
        taxon_id = d['taxon_id']
        if taxon_id is not None:
            try:
                taxon_upper_name = upper_taxo_map[str(taxon_id)]
            except KeyError as e:
                taxon_upper_name = 'Unidentified'
        else:
            taxon_upper_name = 'Unidentified'
        try:
            csv_data[taxon_upper_name] = csv_data[taxon_upper_name] + 1
        except KeyError as k:
            csv_data[taxon_upper_name] = 1
    # And now, write csv
    with open(settings.home_dir + 'class_data.csv', 'w') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        keys = csv_data.keys()
        for key in keys:
            f_writer.writerow([key,csv_data[key]])
    print(csv_data)


def main():
    #auth_data = auth()
    #obs = get_project_observations(settings.api_project_id, auth_data['access_token'])

    #with open( settings.home_dir + 'data.json', 'w') as outfile:
        #json.dump(obs, outfile)

    with open(settings.home_dir + 'data_agustiescobar.json') as f:
        data = json.load(f)

    #write_heatmap_data(data)
    #write_csv_time_histo_15(data)
    #write_csv_time_histo_year(data)
    write_csv_class_histo(data)


if __name__ == '__main__':
    main()
