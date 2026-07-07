# Canadian identifier specifications — provenance

One document per Canadian recognizer (plan item 3.8). Each records the
authoritative source for the identifier's format, the exact rule this
package implements (pattern + validator), and known gaps between the two.

Purpose: the checksum and structure rules in `src/presidio_recognizers_ca_in/`
should be auditable against official documentation, not folklore. When a rule
cannot be sourced from an official publication, the doc says so explicitly.

| Doc | Entity | Recognizer | Validation |
| --- | --- | --- | --- |
| [ca_sin.md](ca_sin.md) | `CA_SIN` | `CaSinRecognizer` | Luhn checksum |
| [ca_ohip.md](ca_ohip.md) | `CA_OHIP` | `OhipRecognizer` | Luhn checksum |
| [ca_ramq.md](ca_ramq.md) | `CA_RAMQ` | `RamqRecognizer` | structural |
| [ca_bc_phn.md](ca_bc_phn.md) | `CA_BC_PHN` | `BcPhnRecognizer` | mod-11 checksum |
| [ca_ab_uli.md](ca_ab_uli.md) | `CA_AB_ULI` | `AlbertaUliRecognizer` | plausibility + context |
| [ca_health_card_generic.md](ca_health_card_generic.md) | `CA_HEALTH_CARD` | `GenericCaHealthCardRecognizer` | context only |
| [ca_postal_code.md](ca_postal_code.md) | `CA_POSTAL_CODE` | `CaPostalCodeRecognizer` | structural (pattern) |
| [ca_street_address.md](ca_street_address.md) | `CA_STREET_ADDRESS` | `CaStreetAddressRecognizer` | structural |

India equivalents (UIDAI, ABDM/NHA, Income Tax Dept, ECI, MEA) are plan
item 4.8 and will be added when the India track opens.
