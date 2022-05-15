#include <iostream>
#include <string>

auto get_string(std::string s) -> std::string { return "Hello, " + s; }

int main() {
  std::cout << get_string("world!") << std::endl;
  return 0;
}