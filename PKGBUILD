# Maintainer: Ma Jiehong <ma dot jiehong on gmail>
pkgname=Zhudi
pkgver=1.4
pkgrel=8
pkgdesc="A Python/GTK3+ GUI and CLO to Chinese -English-French-German dictionnaries (CEDICT, CFDICT, HanDeDict, ChE-Dicc…). It also provides pinyin and zhuyin pronunciaton as well as a sentence segmentation utility."
arch=('any')
url="https://github.com/Jiehong/Zhudi"
license=('GPL3')
depends=('python' 'python-gobject' 'pygobject-devel' 'gobject-introspection' 'pango')
install=zhudi.install
changelog=
source=(git+https://github.com/moorchegue/Zhudi.git)
md5sums=('SKIP')

package() {
    cd "$srcdir/$pkgname"
    msg "Installation in progress…"
    python setup.py install --prefix=/usr --root="$pkgdir/" --optimize=1
}
