#ifndef EXAMPLE_HELLOWORD_HPP
#define EXAMPLE_HELLOWORD_HPP

#include <iostream>
#include <string>

auto get_string(std::string s) -> std::string { return "Hello world, " + s; }

#endif