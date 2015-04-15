# Copyright (C) 2015 Accuvant, Inc. (bspengler@accuvant.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

class BadCerts(Signature):
    name = "bad_certs"
    description = "The executable used a known stolen/malicious Authenticode signature"
    severity = 3
    categories = ["static"]
    authors = ["Accuvant"]
    minimum = "1.3"

    def run(self):
        md5_indicators = []
        sha1_indicators = [
            # Buhtrap from http://www.welivesecurity.com/2015/04/09/operation-buhtrap/
            "cf5a43d14c6ad0c7fdbcbe632ab7c789e39443ee",
            "e9af1f9af597a9330c52a7686bf70b0094ad7616",
            "3e1a6e52a1756017dd8f03ff85ec353273b20c66",
            "efad94fc87b2b3a652f1a98901204ea8fbeef474",
            ]
        if "static" in self.results:
            if "digital_signers" in self.results["static"]:
                for sign in self.results["digital_signers"]:
                    for md5 in md5_indicators:
                        if md5 == sign["md5_fingerprint"]:
                            self.data.append(sign)
                            return True
                    for sha1 in sha1_indicators:
                        if sha1 == sign["sha1_fingerprint"]:
                            self.data.append(sign)
                            return True

        return False