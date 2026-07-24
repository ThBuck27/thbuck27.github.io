// Tyler Buck
// SNHU CS-300
// October 13th, 2025
// Project Two ABCU Advising Assistance Program

//This program is designed to assist students in planning their academic journey by providing information on course prerequisites, degree requirements, and scheduling options.
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cctype>
#include <stdexcept>


using namespace std;

struct Course {
	string id;					//CSCI101
	string title;				//"data structures"
	vector<string> prereqs;		//example: {"CSCI101", "MATH201"}
};

//trim helpers (L/R/Both)
static inline void ltrim(string& s) {
	s.erase(s.begin(), find_if(s.begin(), s.end(), [](unsigned char ch) {
		return !isspace(ch);}));
}
static inline void rtrim(string& s) {
	s.erase(find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
		return !isspace(ch); }).base(), s.end());
}
static inline void trim(string& s) {
	ltrim(s);
	rtrim(s);
}

//Uppercase copy
static inline string upper_copy(string s) {
	for (auto& c : s) c = (char)toupper((unsigned char)c);
	return s;
}

//CSV safe getline for single line split by comma
static vector<string> split_csv_sample(const string& line) {
	vector<string> out; 
	string field;
	stringstream ss(line);
	while (std::getline(ss, field, ',')) {
		trim(field);
		out.push_back(field);
	}
	return out;
}

class CourseCatalog {
public:
	//load from CSV path; returns # of courses loaded; runtime_error on fatal error
	size_t loadFromCSV(const string& path) {
		clear();
		ifstream fin(path);
		if (!fin.is_open()) {
			throw runtime_error("Could not open file: " + path);
		}
		string line;
		size_t lineNo = 0;
		while (std::getline(fin, line)) {
			++lineNo;
			//Skip empty lines
			string tmp = line;
			trim(tmp);
			if (tmp.empty()) continue;

			auto cols = split_csv_sample(line);
			if (cols.size() < 2) {
				cerr << "Warning: line " << lineNo << " has <2 columns; skipping.\n";
				continue;
			}

			Course c;
			c.id = upper_copy(cols[0]);
			c.title = cols[1];
			//remaining columns (if any) are prereqs; ignore blanks
			for (size_t i = 2; i < cols.size(); ++i) {
				if (!cols[i].empty()) c.prereqs.push_back(upper_copy(cols[i]));
			}

			//insert (last one wins if duplicate)
			courses[c.id] = std::move(c);
		}
		fin.close();
		return courses.size();
	}

	bool hasData() const {
		return !courses.empty();
	}

	//return ids sorted alphanumeric
	vector<string> sortedIds() const {
		vector<string> ids;
		ids.reserve(courses.size());
		for (auto& kv : courses) ids.push_back(kv.first);
		sort(ids.begin(), ids.end());
		return ids;
	}

	//print full course list as "ID, Title"
	void printCourseList(std::ostream& os) const {
		auto ids = sortedIds();
		os << "\nHere is a sample schedule:\n\n";
		for (auto& id : ids) {
			auto it = courses.find(id);
			if (it != courses.end()) {
				os << it->second.id << ", " << it->second.title << "\n\n";
			}
		}
	}

	//print info for specific course; title + prereqs w/ # and Title (if avail)
	bool printCourseInfo(const string& queryId, std::ostream& os) const {
		string id = upper_copy(queryId);
		auto it = courses.find(id);
		if (it == courses.end()) {
			return false;
		}
		const Course& c = it->second;
		os << c.id << ", " << c.title << "\n\n";
		if (c.prereqs.empty()) {
			os << "Prerequisites: None\n";
		}
		else {
			os << "Prerequisites: ";
			for (size_t i = 0; i < c.prereqs.size(); ++i) {
				const string &pid = c.prereqs[i];
				auto pit = courses.find(pid);
				if (pit != courses.end()) {
					os << pit->second.id << " (" << pit->second.title << ")";
				}
				else {
					os << pid; //unknown title
				}
				if (i + 1 < c.prereqs.size()) os << ", ";
			}
			os << "\n";
		}
		return true;
	}

private:
	unordered_map<string, Course> courses; //fast lookup by ID
	void clear() {
		courses.clear();
	}
};

//simple menu rendering
static void printMenu() {
	cout << "\n1. Load Data Structure." << "\n";
	cout << "2. Print Course List." << "\n";
	cout << "3. Print Course." << "\n";
	cout << "9. Exit" << "\n\n";
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	cout << "Welcome to the ABCU Course Planner!\n\n";

	CourseCatalog catalog;
	bool loaded = false;

	while (true) {
		printMenu();
		cout << "What would you like to do? ";
		string choice;
		if (!getline(cin, choice)) {
			cout << "\nInput error. Exiting.\n";
			break;
		}
		trim(choice);
		if (choice.empty()) {
			cout << "Please enter a choice.\n";
			continue;
		}
		if (choice == "1") {
			cout << "\nEnter the path to the course CSV file: ";
			string path; getline(cin, path); trim(path);
			try {
				size_t n = catalog.loadFromCSV(path);
				loaded = catalog.hasData();
				cout << "Loaded " << n << " courses.\n";
			}
			catch (const exception& ex) {
				loaded = false;
				cout << "Error: " << ex.what() << "\n";
			}
		}
		else if (choice == "2") {
			if (!loaded) {
				cout << "Please load data first (option 1).\n";
				continue;
			}
			catalog.printCourseList(cout);
		}
		else if (choice == "3") {
			if (!loaded) {
				cout << "Please load data first (option 1).\n";
				continue;
			}
			cout << "\nWhat course do you want to know about? ";
			string id;
			getline(cin, id);
			trim(id);
			if (id.empty()) {
				cout << "Please enter a course ID.\n";
				continue;
			}
			bool ok = catalog.printCourseInfo(id, cout);
			if (!ok) {
				cout << upper_copy(id) << " not found in the catalog.\n";
			}
		}
		else if (choice == "9") {
			cout << "\nThank you for using the ABCU Course Planner. \nGoodbye!\n";
			break;
		}
		else {
			cout << "Invalid choice. Please try again.\n";
		}
	}
	return 0;
}