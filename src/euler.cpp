
#include <iostream>
#include <fstream>
#include <cmath>
#include <string>

int main() {

	double dt;
	int nsteps;

	std::ifstream params("params.dat");
	if (!params.is_open()) {
		std::cerr << "Error: cannot open params.dat\n";
		return 1;
	}


	std::string key;
	while (params >> key) {
		if (key == "dt") params >> dt;
		else if (key == "nsteps") params >> nsteps;
	}
	params.close();


	std::ofstream out("output.dat");
	if (!out.is_open()) {
		std::cerr << "Error: cannot open output.dat\n";
		return 1;
	}

	out << "#t\t\tx_numerical\t\tx_analytical\n";

	double t = 0.0;
	double x = 1.0;


	for (int i = 0; i <= nsteps; ++i) {
		double x_exact = std:: exp(-3.0 * t);
		out << t <<  "\t\t" << x <<  "\t\t" << x_exact << "\n";
		x = (1.0 - 3.0 * dt) * x;
		t += dt;
	}

	out.close();
	std::cout << "Done. dt=" << dt << " nsteps=" << nsteps << "\n";
	return 0;

}
