#include "maccivet.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    maccivet w;
    w.show();

    return a.exec();
}
