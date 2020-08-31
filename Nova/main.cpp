#include "Nova.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Nova w;
    w.show();
    return a.exec();
}
